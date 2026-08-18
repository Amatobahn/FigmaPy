from __future__ import annotations

import asyncio

import httpx
import pytest

import figmapy
from figmapy.errors import (
    FigmaAuthError,
    FigmaError,
    FigmaNotFoundError,
    FigmaRateLimitError,
    FigmaServerError,
    FigmaSpecWarning,
    FigmaValidationError,
)


def json_ok(payload):
    return lambda request: httpx.Response(200, json=payload)


# -- auth -------------------------------------------------------------------


def test_personal_access_token_header(make_client):
    seen = {}

    def handler(request):
        seen.update(request.headers)
        return httpx.Response(200, json={"id": "1", "email": "a@b.c", "handle": "a", "img_url": ""})

    make_client(handler).get_me()
    assert seen["x-figma-token"] == "figd_test"
    assert "authorization" not in seen


def test_oauth2_bearer_header(make_client):
    seen = {}

    def handler(request):
        seen.update(request.headers)
        return httpx.Response(200, json={"id": "1", "email": "a@b.c", "handle": "a", "img_url": ""})

    make_client(handler, oauth2=True).get_me()
    assert seen["authorization"] == "Bearer figd_test"


def test_token_falls_back_to_env(monkeypatch):
    monkeypatch.setenv("FIGMA_TOKEN", "from_env")
    client = figmapy.Figma()
    assert client.headers["X-Figma-Token"] == "from_env"
    client.close()


def test_missing_token_is_a_clear_error(monkeypatch):
    monkeypatch.delenv("FIGMA_TOKEN", raising=False)
    with pytest.raises(FigmaError, match="FIGMA_TOKEN"):
        figmapy.Figma()


# -- parameters -------------------------------------------------------------


def test_unset_params_are_not_sent(make_client, file_payload):
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        return httpx.Response(200, json=file_payload)

    make_client(handler).get_file("KEY", depth=2)
    assert "depth=2" in seen["url"]
    assert "version" not in seen["url"]


def test_list_params_are_joined_with_commas(make_client):
    seen = {}

    def handler(request):
        seen["ids"] = request.url.params["ids"]
        return httpx.Response(200, json={"err": None, "images": {}})

    make_client(handler).get_images("KEY", ids=["1:2", "1:3"])
    assert seen["ids"] == "1:2,1:3"


def test_body_drops_unset_fields(make_client):
    seen = {}

    def handler(request):
        seen["body"] = request.read().decode()
        return httpx.Response(200, json={"id": "c1", "file_key": "KEY", "parent_id": "",
                                         "user": {"id": "1", "handle": "a", "img_url": ""},
                                         "created_at": "2026-01-01T00:00:00Z", "message": "hi",
                                         "order_id": "1", "reactions": [], "client_meta": {"x": 0, "y": 0}})

    make_client(handler).post_comment("KEY", message="hi")
    assert "comment_id" not in seen["body"]
    assert '"message": "hi"' in seen["body"] or '"message":"hi"' in seen["body"]


# -- errors -----------------------------------------------------------------


@pytest.mark.parametrize(
    "status,expected",
    [(403, FigmaAuthError), (404, FigmaNotFoundError), (429, FigmaRateLimitError), (500, FigmaServerError)],
)
def test_status_codes_map_to_typed_errors(make_client, status, expected):
    client = make_client(lambda r: httpx.Response(status, json={"err": "nope"}), max_retries=0)
    with pytest.raises(expected) as exc:
        client.get_file("KEY")
    assert exc.value.status_code == status
    assert exc.value.message == "nope"


def test_retries_429_then_succeeds(make_client, file_payload, monkeypatch):
    monkeypatch.setattr("time.sleep", lambda _: None)
    calls = []

    def handler(request):
        calls.append(1)
        if len(calls) < 3:
            return httpx.Response(429, headers={"Retry-After": "0"}, json={"err": "slow down"})
        return httpx.Response(200, json=file_payload)

    file = make_client(handler, max_retries=3).get_file("KEY")
    assert len(calls) == 3
    assert file.name == "Untitled"


def test_retries_are_bounded(make_client, monkeypatch):
    monkeypatch.setattr("time.sleep", lambda _: None)
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(503, json={"err": "down"})

    with pytest.raises(FigmaServerError):
        make_client(handler, max_retries=2).get_file("KEY")
    assert len(calls) == 3  # initial attempt + 2 retries


def test_404_is_not_retried(make_client, monkeypatch):
    monkeypatch.setattr("time.sleep", lambda _: None)
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(404, json={"err": "gone"})

    with pytest.raises(FigmaNotFoundError):
        make_client(handler, max_retries=3).get_file("KEY")
    assert len(calls) == 1


# -- staying unblocked when the spec is behind -------------------------------


def test_unknown_response_fields_are_kept(make_client, file_payload):
    file_payload["somethingFigmaShippedToday"] = 42
    file = make_client(json_ok(file_payload)).get_file("KEY")
    assert file.somethingFigmaShippedToday == 42


def test_schema_mismatch_warns_and_returns_raw_dict(make_client, file_payload):
    del file_payload["role"]  # pretend Figma made a required field optional
    client = make_client(json_ok(file_payload))
    with pytest.warns(FigmaSpecWarning, match="out of date"):
        result = client.get_file("KEY")
    assert isinstance(result, dict)
    assert result["name"] == "Untitled"


def test_strict_mode_raises_on_schema_mismatch(make_client, file_payload):
    del file_payload["role"]
    with pytest.raises(FigmaValidationError):
        make_client(json_ok(file_payload), strict=True).get_file("KEY")


def test_parse_false_always_returns_dicts(make_client, file_payload):
    result = make_client(json_ok(file_payload), parse=False).get_file("KEY")
    assert isinstance(result, dict)


def test_raw_request_escape_hatch(make_client):
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        return httpx.Response(200, json={"anything": True})

    result = make_client(handler).request("GET", "/v1/not_wrapped_yet", params={"a": 1})
    assert result == {"anything": True}
    assert seen["url"] == "https://api.figma.com/v1/not_wrapped_yet?a=1"


def test_raw_request_accepts_absolute_url(make_client):
    """Pagination `next_page` values are absolute URLs."""
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        return httpx.Response(200, json={})

    make_client(handler).request("GET", "https://api.figma.com/v1/teams/1/components?after=5")
    assert seen["url"].endswith("after=5")


# -- backwards compatibility with figmapy 2018.1.0 ---------------------------


def test_legacy_key_kwarg(make_client, file_payload):
    assert make_client(json_ok(file_payload)).get_file(key="KEY").name == "Untitled"


def test_legacy_get_file_images_alias(make_client):
    result = make_client(json_ok({"err": None, "images": {"1:2": "https://x"}})).get_file_images(
        "KEY", ids=["1:2"]
    )
    assert result.images == {"1:2": "https://x"}


def test_legacy_class_name():
    assert figmapy.FigmaPy is figmapy.Figma


# -- async ------------------------------------------------------------------


def test_async_client_mirrors_sync(file_payload):
    async def main():
        transport = httpx.MockTransport(json_ok(file_payload))
        async with figmapy.AsyncFigma("t", http_client=httpx.AsyncClient(transport=transport)) as figma:
            file = await figma.get_file("KEY")
            legacy = await figma.get_file(key="KEY")
        return file, legacy

    file, legacy = asyncio.run(main())
    assert file.name == legacy.name == "Untitled"


def test_async_retries(file_payload):
    calls = []

    def handler(request):
        calls.append(1)
        if len(calls) < 2:
            return httpx.Response(429, headers={"Retry-After": "0"}, json={})
        return httpx.Response(200, json=file_payload)

    async def main():
        transport = httpx.MockTransport(handler)
        async with figmapy.AsyncFigma("t", http_client=httpx.AsyncClient(transport=transport)) as figma:
            return await figma.get_file("KEY")

    assert asyncio.run(main()).name == "Untitled"
    assert len(calls) == 2
