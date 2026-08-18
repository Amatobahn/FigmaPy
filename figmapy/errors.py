"""Exceptions and warnings raised by figmapy."""

from __future__ import annotations

from typing import Any


class FigmaError(Exception):
    """Base class for every error raised by figmapy."""


class FigmaHTTPError(FigmaError):
    """The Figma API returned a non-2xx status."""

    def __init__(self, status_code: int, message: str, body: Any = None, url: str = ""):
        self.status_code = status_code
        self.message = message
        self.body = body
        self.url = url
        super().__init__(f"{status_code} {message} ({url})" if url else f"{status_code} {message}")


class FigmaAuthError(FigmaHTTPError):
    """401 / 403 - the token is missing, invalid, or lacks the required scope."""


class FigmaNotFoundError(FigmaHTTPError):
    """404 - the file, node, team or project does not exist or is not visible to the token."""


class FigmaRateLimitError(FigmaHTTPError):
    """429 - rate limited, and retries were exhausted."""

    def __init__(self, *args: Any, retry_after: float | None = None, **kwargs: Any):
        self.retry_after = retry_after
        super().__init__(*args, **kwargs)


class FigmaServerError(FigmaHTTPError):
    """5xx - Figma is having a bad day, and retries were exhausted."""


class FigmaSpecWarning(UserWarning):
    """A response did not match the bundled OpenAPI spec.

    Raised as a warning rather than an error so a Figma API change never blocks you:
    the raw ``dict`` is returned instead of a model. Pass ``strict=True`` to the client
    to turn this into a :class:`FigmaValidationError` instead.
    """


class FigmaValidationError(FigmaError):
    """A response did not match the bundled spec, and the client is in strict mode."""


_STATUS_ERRORS = {
    401: FigmaAuthError,
    403: FigmaAuthError,
    404: FigmaNotFoundError,
    429: FigmaRateLimitError,
}


def error_for_status(status_code: int) -> type:
    if status_code in _STATUS_ERRORS:
        return _STATUS_ERRORS[status_code]
    if status_code >= 500:
        return FigmaServerError
    return FigmaHTTPError
