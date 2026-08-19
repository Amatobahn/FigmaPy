"""Hand written conveniences that no OpenAPI spec can generate.

Kept as plain functions rather than model methods: the models are regenerated on every
spec sync, so anything attached to them would be overwritten. Functions survive.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Iterator
from typing import Any

__all__ = [
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

_FILE_KEY = re.compile(r"figma\.com/(?:file|design|board|proto|slides)/([0-9A-Za-z]+)")


def file_key_from_url(url: str) -> str:
    """Pull the file key out of any Figma URL.

    >>> file_key_from_url("https://www.figma.com/design/aBc123XyZ/My-File?node-id=1-2")
    'aBc123XyZ'
    """
    match = _FILE_KEY.search(url)
    if not match:
        raise ValueError(f"No Figma file key found in {url!r}")
    return match.group(1)


def node_id_from_url(url: str) -> str | None:
    """Pull the node id out of a Figma URL, in the `1:2` form the API expects.

    Figma writes node ids as `1-2` in URLs but `1:2` in the API. Returns None if the
    URL has no `node-id`.

    >>> node_id_from_url("https://www.figma.com/design/aBc/My-File?node-id=1-2")
    '1:2'
    """
    match = re.search(r"[?&]node-id=([^&]+)", url)
    if not match:
        return None
    return match.group(1).replace("-", ":", 1)


def _children(node: Any) -> Iterable[Any]:
    return getattr(node, "children", None) or ()


def walk(node: Any, *, include_self: bool = False) -> Iterator[Any]:
    """Yield every descendant of a node, depth first.

    Works on a document, a page, or any container node. Also accepts the object
    returned by ``get_file`` (walks its ``document``).

    >>> for node in walk(file.document):
    ...     print(node.name)
    """
    node = getattr(node, "document", node)
    if include_self:
        yield node
    for child in _children(node):
        yield child
        yield from walk(child)


def _matching(
    root: Any,
    name: str | None,
    type: str | None,
    where: Callable[[Any], bool] | None,
) -> Iterator[Any]:
    for node in walk(root):
        if name is not None and getattr(node, "name", None) != name:
            continue
        if type is not None and getattr(node, "type", None) != type:
            continue
        if where is not None and not where(node):
            continue
        yield node


def find_all(
    root: Any,
    *,
    name: str | None = None,
    type: str | None = None,
    where: Callable[[Any], bool] | None = None,
) -> list:
    """Every descendant of `root` matching all the given filters.

    >>> find_all(file.document, type="TEXT")
    >>> find_all(file.document, name="Icon/Close")
    >>> find_all(file.document, where=lambda n: n.name.startswith("btn_"))
    """
    return list(_matching(root, name, type, where))


def find(
    root: Any,
    *,
    name: str | None = None,
    type: str | None = None,
    where: Callable[[Any], bool] | None = None,
) -> Any | None:
    """The first descendant matching the filters, or None. Same filters as `find_all`."""
    return next(_matching(root, name, type, where), None)


def pages(file: Any) -> list:
    """The pages (CANVAS nodes) of a file."""
    return list(_children(getattr(file, "document", file)))


def page(file: Any, name: str) -> Any | None:
    """A page by name, or None."""
    for candidate in pages(file):
        if getattr(candidate, "name", None) == name:
            return candidate
    return None


def image_urls(client: Any, file_key: str, nodes: Iterable[Any], **kwargs: Any) -> Any:
    """Render a batch of nodes and get back {node_id: url}.

    One request for the whole batch, which is what you want -- rendering nodes one at a
    time is the fastest way to get rate limited.

    >>> image_urls(figma, key, find_all(file.document, type="COMPONENT"), format="svg")
    """
    ids = [node.id for node in nodes]
    if not ids:
        return {}
    result = client.get_images(file_key, ids=ids, **kwargs)
    return getattr(result, "images", None) if not isinstance(result, dict) else result.get("images")


def iter_pages(method: Callable[..., Any], **kwargs: Any) -> Iterator[Any]:
    """Follow the `cursor` / `next_page` pagination used by the analytics and
    activity-log endpoints, yielding one response per page.

    >>> for page in iter_pages(figma.get_library_analytics_component_actions,
    ...                        file_key=key, group_by="component"):
    ...     print(len(page.rows))
    """
    while True:
        response = method(**kwargs)
        yield response
        as_dict = response if isinstance(response, dict) else response.model_dump()
        cursor = as_dict.get("cursor")
        if not as_dict.get("next_page") or not cursor:
            return
        kwargs["cursor"] = cursor
