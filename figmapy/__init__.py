"""figmapy - an unofficial Python wrapper for the Figma REST API.

The client surface and every response model are generated from Figma's official
OpenAPI spec (https://github.com/figma/rest-api-spec), so this package tracks the API
instead of chasing it. ``figmapy.FIGMA_SPEC_VERSION`` tells you which spec release you
have; the package version is the same number.

    import figmapy

    figma = figmapy.Figma(token="figd_...")        # or set FIGMA_TOKEN
    file = figma.get_file("aBc123XyZ")
    for text in figmapy.find_all(file.document, type="TEXT"):
        print(text.characters)
"""

from . import helpers, models
from ._endpoints import FIGMA_SPEC_VERSION
from .client import AsyncFigma, Figma
from .errors import (
    FigmaAuthError,
    FigmaError,
    FigmaHTTPError,
    FigmaNotFoundError,
    FigmaRateLimitError,
    FigmaServerError,
    FigmaSpecWarning,
    FigmaValidationError,
)
from .helpers import (
    file_key_from_url,
    find,
    find_all,
    image_urls,
    iter_pages,
    node_id_from_url,
    page,
    pages,
    walk,
)

__version__ = FIGMA_SPEC_VERSION
__license__ = "Apache-2.0"

#: Pre-1.0 name for :class:`Figma`.
FigmaPy = Figma

__all__ = [
    "Figma",
    "AsyncFigma",
    "FigmaPy",
    "FIGMA_SPEC_VERSION",
    "__version__",
    "models",
    "helpers",
    "FigmaError",
    "FigmaHTTPError",
    "FigmaAuthError",
    "FigmaNotFoundError",
    "FigmaRateLimitError",
    "FigmaServerError",
    "FigmaSpecWarning",
    "FigmaValidationError",
    "file_key_from_url",
    "node_id_from_url",
    "walk",
    "find",
    "find_all",
    "pages",
    "page",
    "image_urls",
    "iter_pages",
]
