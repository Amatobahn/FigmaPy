# Notes for agents working on this repository

Read this before editing. It is short on purpose.

## The one rule

`figmapy/models.py` and `figmapy/_endpoints.py` are **generated**. Never edit them.
Change `tools/generate.py` and run `python tools/generate.py`.

A test fails if the checked-in generated files do not match `spec/openapi.yaml`, so a
hand-edit will be caught, but it wastes a cycle.

## Layout

```
spec/openapi.yaml      Figma's official spec, vendored. The input to everything.
spec/VERSION           Which release. The package version is this number.
tools/generate.py      spec -> the two generated modules
tools/sync_spec.py     fetch a newer spec, regenerate, write a diff report
figmapy/client.py      hand written: auth, transport, retries, error mapping
figmapy/errors.py      hand written: the exception hierarchy
figmapy/helpers.py     hand written: tree walking, URL parsing, batching
figmapy/_compat.py     hand written: names kept from 2018.1.0
tests/                 offline, every request mocked with httpx.MockTransport
```

## Setup

```
pip install -e ".[dev]"
pytest -q
ruff check .
```

No Figma token is needed for anything in this repository, including the tests. If you
find yourself wanting one, you are testing Figma rather than this package.

## Design commitments

These are the decisions the rewrite is built on. Do not quietly undo them.

1. **Generated over hand-written.** The old version fell out of date because keeping up
   meant editing 900 lines of hand-mirrored schema. Anything the spec can describe is
   generated. Anything it cannot is hand-written and small.
2. **A stale release is never a wall.** Unknown response fields are kept
   (`extra="allow"`). A validation failure warns and returns the raw dict rather than
   raising. `client.request()` reaches any endpoint, generated or not. `client.http` is
   the raw httpx client. Do not add a code path that can trap a user behind a missing
   wrapper.
3. **Sync and async render from the same template.** If you add something to one, it must
   come from the generator, not from a second hand-written class.
4. **Helpers are free functions, not model methods.** Models are overwritten on every
   sync; anything attached to them dies.
5. **The version is the spec version.** See `docs/versioning.md`.

## Fixing a failed spec-sync pull request

`.github/workflows/spec-sync.yml` opens these weekly. The body is a generated diff, and
its **Breaking** section is what needs judgement.

1. `git fetch && git checkout spec-sync/<version>`
2. `pip install -e ".[dev]" && pytest -q` to see the actual failure.
3. Most failures are one of:
   - **A test fixture no longer validates.** Figma added a required field. Add it to the
     fixture in `tests/conftest.py`. Do not loosen the model.
   - **A hand-written helper assumed a field that moved.** Fix the helper.
   - **The generator hit a construct it does not handle.** Teach `tools/generate.py` that
     one construct. `py_type()` falling back to `Any` is always an acceptable outcome —
     a loose type never blocks a caller, a crash does.
   - **A name in `_compat.py` now shadows a real generated method.** Check the MRO in
     `client.py`: `LegacyAliases` sits *before* the generated endpoints deliberately.
4. Add a `CHANGELOG.md` entry for anything breaking, and a shim in `_compat.py` if an old
   name is worth keeping alive.
5. Push to the same branch. Do not open a new pull request.

## Style

- Match the surrounding code. It is plain, typed, and comments explain *why*, not *what*.
- `ruff check .` must pass. Line length 110.
- Non-trivial logic leaves a test behind. Tests are offline and use the fixtures in
  `tests/conftest.py`.
- Commits are authored `Claude <noreply@anthropic.com>`.

## Do not

- add a dependency for something httpx, pydantic or the stdlib already does
- add an abstraction with one implementation
- reintroduce a module-level client singleton (the old `session/current.py`)
- make a test require the network or a token
