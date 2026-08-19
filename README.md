# FigmaPy

An unofficial Python wrapper for the [Figma REST API](https://www.figma.com/developers/api).

Every endpoint and every response model is generated from [Figma's official OpenAPI
spec](https://github.com/figma/rest-api-spec), so the wrapper tracks the API instead of
chasing it. All 54 operations are covered, sync and async, with type hints.

```python
import figmapy

figma = figmapy.Figma(token="figd_...")          # or set FIGMA_TOKEN

file = figma.get_file("aBc123XyZ")
for text in figmapy.find_all(file.document, type="TEXT"):
    print(text.characters)
```

## Install

```
pip install FigmaPy
```

Python 3.10+. Depends on `httpx` and `pydantic`.

## Getting a token

A personal access token from [Figma account settings](https://www.figma.com/developers/api#access-tokens)
is enough for most scripts:

```python
figma = figmapy.Figma("figd_...")
figma = figmapy.Figma()                          # reads FIGMA_TOKEN from the environment
figma = figmapy.Figma(oauth_token, oauth2=True)  # OAuth2 access token instead
```

## What you can call

Method names come straight from the spec's operation ids, converted to snake_case:
`get_file`, `get_file_nodes`, `get_images`, `get_team_projects`, `post_comment`,
`get_local_variables`, `get_dev_resources`, and so on. Your editor will autocomplete
them, and each one carries the endpoint's own documentation as a docstring.

```python
figma.get_file_nodes("aBc123XyZ", ids=["1:2", "1:3"])
figma.get_images("aBc123XyZ", ids=["1:2"], format="svg", scale=2)
figma.post_comment("aBc123XyZ", message="ship it")
figma.get_team_projects("1234567890")
```

List arguments are joined with commas for you. Arguments you leave out are not sent.

## Async

The async client is the same surface with `await` in front of it. It is generated from
the same template as the sync one, so the two can never drift apart.

```python
import asyncio, figmapy

async def main():
    async with figmapy.AsyncFigma() as figma:
        keys = ["aBc", "dEf", "gHi"]
        files = await asyncio.gather(*(figma.get_file(k) for k in keys))
        return [f.name for f in files]

asyncio.run(main())
```

Use it when you are fetching many files at once. For a single request it buys nothing —
use `Figma`.

## Walking a file

Figma files are deeply nested trees. These helpers are plain functions, so they keep
working across regenerations:

```python
from figmapy import file_key_from_url, find, find_all, pages, page, walk, image_urls

key = file_key_from_url("https://www.figma.com/design/aBc123XyZ/My-File?node-id=1-2")
file = figma.get_file(key)

pages(file)                                       # the CANVAS nodes
page(file, "Icons")                               # one page by name
find(file.document, name="Button/Primary")        # first match, or None
find_all(file.document, type="COMPONENT")         # every match
find_all(file.document, where=lambda n: n.name.startswith("btn_"))

for node in walk(file.document):                  # everything, depth first
    print(node.type, node.name)

# One request for the whole batch, not one per node.
urls = image_urls(figma, key, find_all(file.document, type="COMPONENT"), format="svg")
```

## Errors

```python
from figmapy import FigmaAuthError, FigmaNotFoundError, FigmaRateLimitError, FigmaHTTPError

try:
    figma.get_file(key)
except FigmaNotFoundError:
    ...          # 404
except FigmaAuthError:
    ...          # 401 / 403, bad token or missing scope
except FigmaRateLimitError as e:
    ...          # 429, and the retries were already exhausted
```

429s and 5xx are retried automatically, honouring `Retry-After` and otherwise backing off
exponentially with jitter. `max_retries=0` turns that off.

## Nothing here should ever block you

Figma ships API changes whenever it likes, and this package will sometimes be a release
behind. That is an inconvenience, never a wall:

| Situation | What happens | Escape hatch |
| --- | --- | --- |
| Response has a field the models do not know | It is kept, and readable as an attribute | none needed |
| Response no longer matches the spec | Warns `FigmaSpecWarning`, returns the raw `dict` | `strict=True` to raise instead |
| You would rather have dicts everywhere | — | `Figma(parse=False)` |
| Endpoint not in your installed version | — | `figma.request("GET", "/v1/whatever", params={...})` |
| Whole client is in your way | — | `figma.http` is the underlying `httpx.Client` |

```python
# An endpoint that shipped after your version of this package
data = figma.request("POST", "/v1/files/aBc/some_new_thing", json_body={"x": 1})
```

If you hit one of these, [open an issue](https://github.com/Amatobahn/FigmaPy/issues) —
but only after you have unblocked yourself with the row above.

## Versioning

The package version follows date-based versioning (`YEAR.RELEASE.PATCH`), continuing the scheme from `FigmaPy 2018.1.0` on PyPI.

```python
figmapy.__version__          # '2026.1.0'
figmapy.FIGMA_SPEC_VERSION   # '0.42.0' - the Figma OpenAPI spec this was generated from
```

See [docs/versioning.md](docs/versioning.md) for the full rules.

## Upgrading from 2018.1.0

See [MIGRATION.md](MIGRATION.md). The short version: `FigmaPy` is now `Figma`, method
names match the spec, and responses are pydantic models. The old names still work.

## Contributing

`figmapy/models.py` and `figmapy/_endpoints.py` are generated — do not edit them, edit
`tools/generate.py` and re-run it. Everything else is fair game. See
[docs/maintenance.md](docs/maintenance.md), and
[docs/review-and-plan.md](docs/review-and-plan.md) for why the repository is shaped this
way.

```
pip install -e ".[dev]"
pytest              # no network needed, every request is mocked
ruff check .
```

## License

Apache-2.0. Originally by [Greg Amato](https://github.com/Amatobahn), with the
generated rewrite contributed later.
