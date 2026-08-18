from __future__ import annotations

import httpx
import pytest

import figmapy
from figmapy import models


@pytest.fixture
def file(file_payload):
    return models.GetFileResponse.model_validate(file_payload)


def test_file_key_from_url():
    urls = [
        "https://www.figma.com/design/aBc123XyZ/My-File?node-id=1-2&t=x",
        "https://www.figma.com/file/aBc123XyZ/My-File",
        "figma.com/board/aBc123XyZ/Jam",
    ]
    assert {figmapy.file_key_from_url(u) for u in urls} == {"aBc123XyZ"}


def test_file_key_from_url_rejects_junk():
    with pytest.raises(ValueError):
        figmapy.file_key_from_url("https://example.com/nope")


def test_node_id_from_url_converts_dash_to_colon():
    assert figmapy.node_id_from_url("https://figma.com/design/k/f?node-id=1-2") == "1:2"
    assert figmapy.node_id_from_url("https://figma.com/design/k/f") is None


def test_walk_visits_every_descendant(file):
    names = [n.name for n in figmapy.walk(file)]
    assert names == ["Page 1", "Title", "Page 2"]


def test_walk_accepts_a_document_or_a_file(file):
    assert list(figmapy.walk(file)) == list(figmapy.walk(file.document))


def test_find_and_find_all(file):
    assert figmapy.find(file, type="TEXT").characters == "Hello"
    assert figmapy.find(file, name="nope") is None
    assert [n.name for n in figmapy.find_all(file, type="CANVAS")] == ["Page 1", "Page 2"]
    assert figmapy.find_all(file, where=lambda n: n.name.endswith("2")) != []


def test_pages_and_page(file):
    assert [p.name for p in figmapy.pages(file)] == ["Page 1", "Page 2"]
    assert figmapy.page(file, "Page 2").id == "0:2"
    assert figmapy.page(file, "Page 9") is None


def test_image_urls_batches_one_request(make_client, file):
    calls = []

    def handler(request):
        calls.append(request.url.params["ids"])
        return httpx.Response(200, json={"err": None, "images": {"1:2": "https://img"}})

    client = make_client(handler)
    urls = figmapy.image_urls(client, "KEY", figmapy.find_all(file, type="TEXT"), format="svg")
    assert urls == {"1:2": "https://img"}
    assert calls == ["1:2"]


def test_image_urls_skips_the_request_when_there_is_nothing_to_render(make_client, file):
    def handler(request):  # pragma: no cover - must not be called
        raise AssertionError("no request should be made")

    assert figmapy.image_urls(make_client(handler), "KEY", []) == {}


def test_iter_pages_follows_the_cursor():
    pages = [
        {"rows": [1], "next_page": True, "cursor": "c1"},
        {"rows": [2], "next_page": True, "cursor": "c2"},
        {"rows": [3], "next_page": False},
    ]
    seen_cursors = []

    def endpoint(**kwargs):
        seen_cursors.append(kwargs.get("cursor"))
        return pages[len(seen_cursors) - 1]

    collected = [p["rows"][0] for p in figmapy.iter_pages(endpoint, file_key="KEY")]
    assert collected == [1, 2, 3]
    assert seen_cursors == [None, "c1", "c2"]
