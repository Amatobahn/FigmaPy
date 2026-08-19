"""The Figma and AsyncFigma clients.

This module is hand written and small on purpose: everything that mirrors the Figma
API surface is generated into ``_endpoints.py`` and ``models.py`` from the official
spec. What lives here is the part a spec cannot describe -- auth, transport, retries,
error mapping and the escape hatches that keep you unblocked when the spec is behind.
"""

from __future__ import annotations

import asyncio
import os
import random
import time
import warnings
from collections.abc import Mapping
from typing import Any

import httpx
from pydantic import ValidationError

from ._compat import LegacyAliases
from ._endpoints import FIGMA_SPEC_VERSION, AsyncEndpoints, SyncEndpoints
from .errors import (
    FigmaError,
    FigmaRateLimitError,
    FigmaSpecWarning,
    FigmaValidationError,
    error_for_status,
)

DEFAULT_BASE_URL = "https://api.figma.com"
TOKEN_ENV_VAR = "FIGMA_TOKEN"
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
MAX_BACKOFF_SECONDS = 60.0


class _BaseClient:
    def __init__(
        self,
        token: str | None = None,
        *,
        oauth2: bool = False,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        strict: bool = False,
        parse: bool = True,
        headers: Mapping[str, str] | None = None,
    ):
        """
        token:       personal access token, or OAuth2 access token when ``oauth2=True``.
                     Falls back to the ``FIGMA_TOKEN`` environment variable.
        oauth2:      send the token as ``Authorization: Bearer`` instead of ``X-Figma-Token``.
        base_url:    override for testing or for a proxy.
        timeout:     per-request timeout in seconds.
        max_retries: retries for 429 and 5xx responses. 0 disables retrying.
        strict:      raise :class:`FigmaValidationError` when a response does not match
                     the bundled spec, instead of warning and returning the raw dict.
        parse:       set False to always get plain dicts back and skip model validation.
        headers:     extra headers merged into every request.
        """
        token = token or os.environ.get(TOKEN_ENV_VAR)
        if not token:
            raise FigmaError(
                f"No Figma token. Pass token=... or set the {TOKEN_ENV_VAR} environment variable. "
                "Personal access tokens are created at https://www.figma.com/developers/api#access-tokens"
            )
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")

        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.strict = strict
        self.parse = parse
        self.spec_version = FIGMA_SPEC_VERSION
        self.timeout = timeout

        auth = {"Authorization": f"Bearer {token}"} if oauth2 else {"X-Figma-Token": token}
        self.headers = {"User-Agent": f"figmapy/{FIGMA_SPEC_VERSION}", **auth, **(headers or {})}

    # -- request building / response handling, shared by both clients -----------

    def _url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    @staticmethod
    def _clean_body(data: Mapping[str, Any] | None) -> dict | None:
        """Drop unset (None) values so we never send `{"passcode": null}`."""
        if not data:
            return None
        return {k: v for k, v in data.items() if v is not None} or None

    @classmethod
    def _clean_params(cls, data: Mapping[str, Any] | None) -> dict | None:
        """Drop unset values, and join lists into the comma form Figma expects.

        Every list-shaped Figma query parameter (`ids`, `plugin_data`, ...) is a comma
        separated string on the wire, so accepting a real list everywhere saves the
        caller a `",".join(...)` and works for parameters added in future spec versions.
        """
        cleaned = cls._clean_body(data)
        if not cleaned:
            return None
        return {
            k: ",".join(str(i) for i in v) if isinstance(v, (list, tuple, set)) else v
            for k, v in cleaned.items()
        }

    def _raise_for_status(self, response: httpx.Response) -> None:
        if response.status_code < 400:
            return
        try:
            body: Any = response.json()
        except ValueError:
            body = response.text
        message = ""
        if isinstance(body, dict):
            message = str(body.get("message") or body.get("err") or body.get("error") or "")
        message = message or response.reason_phrase or "request failed"

        cls: type[Any] = error_for_status(response.status_code)
        kwargs: dict = {}
        if cls is FigmaRateLimitError:
            kwargs["retry_after"] = _retry_after(response)
        raise cls(response.status_code, message, body=body, url=str(response.url), **kwargs)

    def _parse(self, data: Any, model: type | None) -> Any:
        if model is None or not self.parse or not isinstance(data, dict):
            return data
        try:
            return model.model_validate(data)
        except ValidationError as exc:
            detail = (
                f"{model.__name__} does not match the response Figma sent. "
                f"figmapy was generated from Figma spec {FIGMA_SPEC_VERSION}; it is probably out of date. "
                f"Returning the raw dict instead.\n{exc}"
            )
            if self.strict:
                raise FigmaValidationError(detail) from exc
            warnings.warn(detail, FigmaSpecWarning, stacklevel=4)
            return data

    def _backoff(self, response: httpx.Response | None, attempt: int) -> float:
        if response is not None:
            explicit = _retry_after(response)
            if explicit is not None:
                return min(explicit, MAX_BACKOFF_SECONDS)
        # full jitter, so a fleet of workers does not retry in lockstep
        return min(2.0**attempt, MAX_BACKOFF_SECONDS) * (0.5 + random.random() / 2)

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        return status_code in RETRY_STATUSES and attempt < self.max_retries


class Figma(_BaseClient, LegacyAliases, SyncEndpoints):
    """Synchronous Figma REST API client.

    >>> import figmapy
    >>> figma = figmapy.Figma(token="figd_...")          # or set FIGMA_TOKEN
    >>> file = figma.get_file("abc123")
    >>> [page.name for page in file.document.children]
    ['Page 1']
    """

    def __init__(self, *args: Any, http_client: httpx.Client | None = None, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._owns_client = http_client is None
        #: The underlying httpx client. Public, so you can reach past the wrapper.
        self.http = http_client or httpx.Client(timeout=self.timeout, follow_redirects=True)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Mapping[str, Any] | None = None,
    ) -> Any:
        """Call any Figma endpoint and get the raw JSON back.

        The escape hatch: if figmapy has no method for something yet, or Figma shipped a
        parameter this release does not know about, you are never blocked.

        >>> figma.request("GET", "/v1/files/abc123", params={"depth": 1})
        """
        return self._call(method, path, params=params, json_body=json_body, model=None)

    def _call(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Mapping[str, Any] | None = None,
        model: type | None = None,
    ) -> Any:
        url = self._url(path)
        attempt = 0
        while True:
            response = self.http.request(
                method,
                url,
                headers=self.headers,
                params=self._clean_params(params),
                json=self._clean_body(json_body),
            )
            if not self._should_retry(response.status_code, attempt):
                break
            time.sleep(self._backoff(response, attempt))
            attempt += 1

        self._raise_for_status(response)
        if not response.content:
            return None
        return self._parse(response.json(), model)

    def close(self) -> None:
        if self._owns_client:
            self.http.close()

    def __enter__(self) -> Figma:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


class AsyncFigma(_BaseClient, LegacyAliases, AsyncEndpoints):
    """Asynchronous Figma REST API client.

    Identical surface to :class:`Figma`, every method awaitable. Both classes are
    generated from the same spec, so async is not a second thing to maintain.

    >>> async with figmapy.AsyncFigma() as figma:
    ...     file = await figma.get_file("abc123")
    """

    def __init__(self, *args: Any, http_client: httpx.AsyncClient | None = None, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._owns_client = http_client is None
        #: The underlying httpx client. Public, so you can reach past the wrapper.
        self.http = http_client or httpx.AsyncClient(timeout=self.timeout, follow_redirects=True)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Mapping[str, Any] | None = None,
    ) -> Any:
        """Call any Figma endpoint and get the raw JSON back. See :meth:`Figma.request`."""
        return await self._call(method, path, params=params, json_body=json_body, model=None)

    async def _call(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_body: Mapping[str, Any] | None = None,
        model: type | None = None,
    ) -> Any:
        url = self._url(path)
        attempt = 0
        while True:
            response = await self.http.request(
                method,
                url,
                headers=self.headers,
                params=self._clean_params(params),
                json=self._clean_body(json_body),
            )
            if not self._should_retry(response.status_code, attempt):
                break
            await asyncio.sleep(self._backoff(response, attempt))
            attempt += 1

        self._raise_for_status(response)
        if not response.content:
            return None
        return self._parse(response.json(), model)

    async def aclose(self) -> None:
        if self._owns_client:
            await self.http.aclose()

    async def __aenter__(self) -> AsyncFigma:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.aclose()


def _retry_after(response: httpx.Response) -> float | None:
    raw = response.headers.get("retry-after")
    if not raw:
        return None
    try:
        return max(0.0, float(raw))
    except ValueError:
        return None  # HTTP-date form; fall back to exponential backoff
