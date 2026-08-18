# Migrating from FigmaPy 2018.1.0

The client surface is now generated from Figma's official OpenAPI spec instead of being
hand-written, which changed some names. Most scripts need a handful of edits; the common
ones still work unchanged.

Python 3.10 or newer is required. `requests` and `aiohttp` are gone, replaced by `httpx`.

## Still works

```python
import figmapy

figma = figmapy.FigmaPy(token)     # FigmaPy is an alias for Figma
figma.get_file(key="aBc123XyZ")    # key= is still accepted
figma.get_file_images(key, ids=["1:2"])
```

`FigmaPy`, the `key=` keyword and `get_file_images` are kept in `figmapy/_compat.py`. They
are not going away, but the new names are the documented ones.

## Client

| 2018.1.0 | now |
| --- | --- |
| `from figmapy import FigmaPy` | `from figmapy import Figma` |
| `from figmapy import AioHttpFigmaPy` | `from figmapy import AsyncFigma` |
| `FigmaPy(token, oauth2=True)` | `Figma(token, oauth2=True)` — unchanged |
| `figma.api_request("v1/files/x", method="get")` | `figma.request("GET", "/v1/files/x")` |
| `figmapy.session.current.figma_session` | gone; pass the client around, or use one of the helpers that takes it |
| `figma.create_token(client_id, ...)` | gone; the OAuth token exchange is not part of Figma's spec. See below. |

The global `figma_session` singleton was what let nodes call back into the API by
themselves. Nothing depends on it now, so it was removed rather than kept as a trap for
multi-account scripts.

The OAuth2 code-for-token exchange is a two-line `httpx.post` and is not a Figma REST API
endpoint, so it is out of scope:

```python
httpx.post("https://api.figma.com/v1/oauth/token", data={
    "client_id": ..., "client_secret": ..., "redirect_uri": ...,
    "code": ..., "grant_type": "authorization_code",
}).json()["access_token"]
```

## Methods

Names now come from the spec's operation ids, so they match Figma's own documentation.

| 2018.1.0 | now |
| --- | --- |
| `get_file(key, geometry, version)` | `get_file(file_key, *, version, ids, depth, geometry, plugin_data, branch_data)` |
| `get_file_nodes(file_key, ids, ...)` | `get_file_nodes(file_key, *, ids, ...)` — `ids` is now keyword-only |
| `get_file_images(file_key, ids, scale, format, version)` | `get_images(file_key, *, ids, scale, format, version, ...)` |
| `get_image_fills(file_key)` | unchanged |
| `get_file_versions(file_key)` | unchanged |
| `get_comments(file_key)` | unchanged |
| `post_comment(file_key, message, client_meta)` | `post_comment(file_key, *, message, client_meta)` |
| `delete_comment()` (never worked) | `delete_comment(file_key, comment_id)` |
| `get_team_projects(team_id)` | unchanged |
| `get_project_files(project_id)` | unchanged |
| `get_vector_images(file_key, nodes, scale, format)` | `figmapy.image_urls(figma, file_key, nodes, scale=..., format=...)` |
| `get_file_images_sync(...)` | gone; `AsyncFigma` and `Figma` are separate classes now |

Optional arguments are keyword-only. `ids` accepts a list and is joined for you.

Nine operations were wrapped before. All 54 are wrapped now — variables, dev resources,
webhooks, activity logs, library analytics, and the rest.

## Responses

Responses used to be bespoke classes from `figmapy.datatypes`. They are pydantic models
generated from the spec, in `figmapy.models`.

```python
# before
from figmapy import datatypes as dt
isinstance(node, dt.Text)

# now
node.type == "TEXT"
```

Attribute access is mostly the same, because both follow Figma's own field names. What
changed:

- `figmapy.datatypes` / `figmapy.dt` → `figmapy.models`
- the node class hierarchy (`Text`, `Frame`, `Vector`, `Component`, ...) is now the
  generated union in `figmapy.models`; branch on `node.type` instead of `isinstance`
- `node._parent` is gone. The spec has no parent pointers and synthesising them meant
  walking every file twice.
- unknown fields are kept instead of dropped, so a field Figma shipped last week is
  readable today

## Node helpers are free functions now

Methods on the node classes would be wiped out on every regeneration, so they moved to
`figmapy.helpers` (re-exported from the package root):

| 2018.1.0 | now |
| --- | --- |
| `node.get_children_recursively()` | `walk(node)` — an iterator, not a list |
| `document.pages()` | `pages(file)` |
| `document.get_page("Icons")` | `page(file, "Icons")` |
| `node.get_file_image_url()` | `image_urls(figma, file_key, [node])[node.id]` |
| `figmapy.utils.get_file_key(node)` | gone with `_parent`; keep the key you fetched with |
| — | `find(root, name=..., type=..., where=...)`, `find_all(...)`, new |
| — | `file_key_from_url(url)`, `node_id_from_url(url)`, new |

```python
from figmapy import walk, find_all, pages, page, image_urls

file = figma.get_file(key)
for node in walk(file.document):
    print(node.type, node.name)

urls = image_urls(figma, key, find_all(file.document, type="COMPONENT"), format="svg")
```

## Errors

The old client printed the failure and returned `None`, so a typo in a file key surfaced
much later as `AttributeError: 'NoneType'`. It now raises:

```python
from figmapy import FigmaNotFoundError, FigmaAuthError, FigmaRateLimitError

try:
    file = figma.get_file(key)
except FigmaNotFoundError:
    ...
```

If you relied on the `None`:

```python
try:
    file = figma.get_file(key)
except figmapy.FigmaHTTPError:
    file = None
```

429s and 5xx are now retried automatically. If your code had its own sleep-and-retry loop,
delete it.

## Async

```python
# before
from figmapy import AioHttpFigmaPy
figma = AioHttpFigmaPy(token)

# now
import asyncio, figmapy

async def main():
    async with figmapy.AsyncFigma(token) as figma:
        return await asyncio.gather(figma.get_file(a), figma.get_file(b))
```

Every sync method has an identical async twin. Both are rendered from the same generator
template, so the async client is no longer a partial reimplementation that lags behind.
