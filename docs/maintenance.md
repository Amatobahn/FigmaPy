# Maintenance

The point of this repository's layout is that keeping up with Figma is a scheduled job,
not a chore. This is what that job does and what is left for a human.

## The moving parts

```
spec/openapi.yaml     Figma's official spec, vendored. The input to everything.
spec/VERSION          Which release of it. Single source of truth for the version.
tools/generate.py     spec -> figmapy/_endpoints.py + figmapy/models.py
tools/sync_spec.py    fetch a newer spec, regenerate, write a diff report
figmapy/*.py          hand written: client, errors, helpers, compat shims
```

Two files are generated and must never be hand-edited:

- `figmapy/_endpoints.py` — `SyncEndpoints` and `AsyncEndpoints`, one method per spec
  operation, both rendered from the same template so they cannot drift.
- `figmapy/models.py` — every response and request schema as a pydantic model.

If either needs to change, change `tools/generate.py` and re-run it. A test
(`test_generated.py::test_checked_in_code_matches_the_spec`) regenerates and fails if the
checked-in files are stale, so this cannot be forgotten.

## The weekly job

`.github/workflows/spec-sync.yml` runs Mondays and on demand. It:

1. compares `spec/VERSION` against the newest tag on `figma/rest-api-spec`
2. downloads the new spec, regenerates both files, bumps the version everywhere
3. writes `docs/spec-changes.md` — added, removed and changed endpoints, added and
   removed fields, and a **Breaking** section
4. runs `ruff` and `pytest`
5. opens a pull request titled `Figma spec <version>` with that report as its body

The pull request is a **draft** if the tests failed or the diff is breaking. Otherwise it
is ready to merge.

## Deciding what to do with the pull request

| Report says | Do |
| --- | --- |
| Green, no breaking section | Merge it. Tag `v<version>`, which releases. |
| Green, breaking section | Read the breaking bullets. Usually Figma deprecating something. Add a shim in `figmapy/_compat.py` if it is worth keeping the old name alive, note it in `CHANGELOG.md`, then merge. |
| Tests failed | Something in the hand-written half assumed a shape the spec no longer has. Fix it in `tools/generate.py` or `figmapy/`, push to the same branch. |
| Generator crashed | The spec used a construct `tools/generate.py` does not handle. See below. |

An agent can do all four. `CLAUDE.md` at the repository root is the briefing for that.

## When the generator crashes

`tools/generate.py` is deliberately small and only understands the subset of OpenAPI that
Figma actually uses. When Figma reaches for something new, the fix is to teach it that
one construct — not to move to a heavyweight generator. The places it makes assumptions:

- `py_type()` — maps a schema to a Python annotation, falling back to `Any`. Falling back
  is always safe; a wrong-but-loose type never blocks a caller.
- `hoist_responses()` — Figma defines response bodies under `components/responses`, where
  `datamodel-code-generator` will not look, so they are copied into `components/schemas`
  first.
- `response_models()` — an operation whose 200 response is a bare `$ref` returns the
  referenced model directly instead of a generated wrapper.
- `_urls_as_str()` — `format: uri` becomes `str`, not pydantic's `AnyUrl`, which
  normalises URLs and would surprise anyone comparing strings.

## Releasing

```
git tag v0.42.0 && git push --tags
```

`.github/workflows/release.yml` checks that the tag matches `figmapy.__version__`, runs
the suite, builds, and publishes to PyPI via trusted publishing. There is no token to
rotate; the publisher is configured once in the PyPI project settings.

## Running it by hand

```
pip install -e ".[dev]"

python tools/sync_spec.py --check          # is there a newer spec?
python tools/sync_spec.py                  # sync to the newest
python tools/sync_spec.py --version 0.43.0 # sync to a specific one
python tools/generate.py                   # regenerate from the vendored spec

pytest -q                                  # no network, every request is mocked
ruff check .
```

## Testing philosophy

No test hits the Figma API. Every request goes through `httpx.MockTransport`, so the suite
runs offline, in CI, in a fork, and on a laptop with no token. That is deliberate: a test
suite that needs a secret is a test suite that contributors skip.

What the tests actually guard:

- the hand-written half — auth, retries, error mapping, parameter cleaning, escape hatches
- the *shape* of the generated half — every spec operation exists, sync and async
  signatures are identical, async methods are coroutines
- that the checked-in generated files match the vendored spec
- that unknown fields survive, and that a schema mismatch degrades instead of raising

Nothing asserts that Figma's own responses match Figma's own spec. That is Figma's job,
and if they diverge, the client warns at runtime rather than failing.
