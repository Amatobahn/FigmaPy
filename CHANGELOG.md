# Changelog

Versions use date-based versioning (`YEAR.RELEASE.PATCH`). See
[docs/versioning.md](docs/versioning.md) for the scheme; `figmapy.FIGMA_SPEC_VERSION`
tells you which Figma OpenAPI spec each release was generated from.

## 2026.1.0

Generated from [rest-api-spec
v0.42.0](https://github.com/figma/rest-api-spec/releases/tag/v0.42.0).

A rewrite. The client surface and every response model now come from Figma's official
OpenAPI spec instead of being hand-mirrored, which is what kept the old version out of
date. See [MIGRATION.md](MIGRATION.md) for upgrading from 2018.1.0.

### Added

- All 54 API operations, up from 9. Variables, dev resources, webhooks, activity logs,
  library analytics, payments, and the rest.
- `AsyncFigma`, an identical awaitable surface rendered from the same generator template
  as the sync client, so the two cannot drift.
- A typed exception hierarchy: `FigmaAuthError`, `FigmaNotFoundError`,
  `FigmaRateLimitError`, `FigmaServerError`, all under `FigmaHTTPError`.
- Automatic retries for 429 and 5xx, honouring `Retry-After` and otherwise backing off
  exponentially with full jitter.
- Escape hatches so a stale release never blocks anyone: unknown response fields are
  kept, a schema mismatch warns and returns the raw dict, `client.request()` reaches any
  endpoint, and `client.http` is the underlying httpx client.
- `strict=True` to turn schema mismatches into errors, and `parse=False` to skip model
  validation entirely.
- Helpers: `walk`, `find`, `find_all`, `pages`, `page`, `image_urls`, `iter_pages`,
  `file_key_from_url`, `node_id_from_url`.
- Token falls back to the `FIGMA_TOKEN` environment variable.
- `tools/sync_spec.py` and a weekly workflow that opens a pull request when Figma ships a
  new spec, with a generated diff and a mechanical breaking-change verdict.
- A test suite that runs offline, with no token, against `httpx.MockTransport`.

### Changed

- `FigmaPy` is now `Figma`; `AioHttpFigmaPy` is now `AsyncFigma`. The old names still
  resolve.
- Method names follow the spec's operation ids, so they match Figma's documentation.
  `get_file_images` is `get_images`; the old name is kept as an alias.
- Responses are pydantic models from `figmapy.models`, not classes from
  `figmapy.datatypes`.
- Node helper methods became free functions, because models are regenerated on every
  spec sync and anything attached to them would be lost.
- Failures raise instead of printing and returning `None`.
- `requests` and `aiohttp` replaced by `httpx`. `pydantic>=2.5` added.
- Python 3.10 or newer.
- Packaging moved from `setup.py` to `pyproject.toml` (hatchling).

### Fixed

- The package is installable again. `setup.py` packaged a `FigmaPy` directory that does
  not exist on disk (the package is lowercase `figmapy`), which is why PyPI has been
  stuck on 2018.1.0 since 2018 while the repository moved on. The async extra was also
  spelled `extra_requires` rather than `extras_require`, so it was silently ignored.
- Query strings and JSON bodies are built by httpx instead of by string concatenation,
  so values containing `&`, `=` or spaces no longer corrupt the request.
- `delete_comment()` took no arguments and could not have worked. It now takes
  `file_key` and `comment_id`.
- The module-level `figma_session` singleton is gone, so two clients in one process no
  longer fight over it.

## 2018.1.0

The original hand-written wrapper by [Greg Amato](https://github.com/Amatobahn).
