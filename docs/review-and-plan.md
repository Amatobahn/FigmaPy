# Review of FigmaPy 2018.1.0, and the plan that replaced it

Written August 2026, before the rewrite in 0.42.0. Kept because the reasoning explains
why the repository is shaped the way it is.

## Strengths worth keeping

- **The idea is right.** A thin typed Python layer over the Figma REST API is genuinely
  useful, and nothing else in the ecosystem fills that slot well.
- **The node tree helpers.** `get_children_recursively`, `pages`, `get_page`,
  `get_vector_images` batching a render call — these are the parts a code generator will
  never produce, and they are what made the library nicer than raw `requests`. They
  survived the rewrite, as free functions.
- **The dataclass-shaped responses.** Attribute access over dict-digging was the correct
  instinct. Only the way they were produced had to change.
- **A real, working async client existed.** Rare in a small wrapper.
- **Sensible repository hygiene** — pre-commit, tests, a licence, a changelog habit.

## Weaknesses

### 1. The schema was hand-mirrored, and that is the whole problem

`datatypes/nodes.py` was 606 lines and `datatypes/properties.py` 292, all of it a
hand-typed copy of Figma's own documentation. Every field Figma shipped was a manual
edit in a file with no way to tell what was missing. Nothing tells you when you fall
behind except a user's bug report, and the work is unbounded, boring and never done.

This is the root cause of "often out of date with the API". Everything below is a
symptom or an aggravation.

### 2. Coverage was 9 operations out of 54

`get_file`, `get_file_nodes`, `get_file_images`, `get_image_fills`, `get_file_versions`,
`get_comments`, `post_comment`, `get_team_projects`, `get_project_files`. Missing:
variables, dev resources, webhooks, activity logs, library analytics, components and
styles, payments — most of what Figma added after 2018. `delete_comment()` took no
arguments and could never have worked.

### 3. The published package was broken for seven years

```python
packages=['FigmaPy'],       # the directory on disk is lowercase `figmapy`
```

`pip install FigmaPy` installed metadata and no code. That is why PyPI still shows
2018.1.0 while the repository kept moving: releasing was broken, so releasing stopped,
so the fix never shipped. The async extra was also spelled `extra_requires` instead of
`extras_require`, so it was silently ignored.

### 4. Errors vanished

```python
except Exception as e:
    print(f'Error: {e}')
    return None
```

A typo in a file key produced `AttributeError: 'NoneType' object has no attribute
'document'` several frames later. No retry on 429, no `Retry-After`, no backoff, and
rate limiting is the single most common thing you hit when scripting Figma.

### 5. Requests were built by hand

Query strings by string concatenation, JSON bodies by f-string. Any value containing
`&`, `=` or a space corrupted the request.

### 6. Global mutable session

`session/current.py` held a module-level `figma_session` so nodes could call back into
the API. Two clients in one process, or two accounts, fought over it.

### 7. Sync and async were separate implementations

`figma_requests.py` and `figma_aiohttp.py` each spelled out the same endpoints. Two
copies of one API means one of them is always behind — and it was. This is why async
*felt* like unnecessary complexity: not because async is wrong, but because it was a
second thing to maintain by hand.

## The plan

### Generate everything the spec can describe

Figma publishes an official, versioned OpenAPI spec at
[figma/rest-api-spec](https://github.com/figma/rest-api-spec) (MIT). It is complete: 47
paths, 54 operations, 230 schemas. It is the artefact the old `datatypes` package was a
worse hand-made copy of.

So: vendor it, and generate from it.

- `figmapy/models.py` — 507 pydantic models, via `datamodel-code-generator`.
- `figmapy/_endpoints.py` — one method per operation, sync and async, from one template
  in `tools/generate.py`.
- Hand-write only what a spec cannot describe: auth, transport, retries, error mapping,
  tree helpers, compatibility shims. That is about 300 lines, and it is stable, because
  none of it changes when Figma adds a field.

Coverage goes from 9 operations to 54, and stays there for free.

### Version = spec version

`FigmaPy 0.42.0` is generated from spec v0.42.0. `figmapy.FIGMA_SPEC_VERSION` says so at
runtime.

This answers "how do I manage this with versioning". Semver would ask a human to judge
each release, and that judgement is exactly the step that stalls — see the seven-year
gap above. Tying the number to the spec removes the judgement, so the release can be
automated end to end. Wrapper-only fixes ship as `.postN` on the current spec version.
Full rules in [versioning.md](versioning.md).

### Make being out of date an inconvenience, never a wall

This is the "how can a user dev without blockers" half, and it matters more than being
up to date, because you will never be up to date on the day Figma ships something.

Every layer of the client is built to degrade rather than refuse:

| Figma changed something | figmapy does |
| --- | --- |
| New field in a response | Keeps it (`extra="allow"`), readable as an attribute |
| Response no longer matches the spec | Warns, returns the raw dict; `strict=True` to raise |
| New endpoint | `client.request("POST", "/v1/anything", ...)` |
| New query parameter | `params=` on the same call |
| The wrapper itself is in the way | `client.http` is the raw httpx client |

An old pin still talks to today's Figma. It just has fewer typed conveniences.

### Automate the upkeep, keep the judgement

A weekly job checks for a new spec release, regenerates, tests, and opens a pull request
with a generated diff. Anything removed or newly required is labelled `breaking` and the
pull request opens as a draft. Additive syncs — which is nearly all of them — are green
and mergeable on sight; tagging releases them.

The classification is mechanical, not model-generated, so it is reproducible. What is
left for a human or an agent is a real judgement: is this breaking change worth a
compatibility shim? `CLAUDE.md` is the briefing for handling exactly that.

### Keep async

The open question was whether async was fancy stuff nobody needed. As it was written:
yes — a hand-maintained duplicate of the sync client is a liability, and for a single
request it buys nothing.

But that cost is gone. Both clients render from the same generator template over httpx's
symmetric sync/async API, so the async surface is a byproduct, not a burden, and it
cannot drift. And there is one case where it genuinely matters: fetching many files, or
rendering many node batches, where the work is entirely network-bound. So it stays.

The rule for users, stated plainly in the README: use `Figma`, unless you are fetching
many things at once.

### Keep the old names working

`FigmaPy`, `key=`, `get_file_images` still work, via `figmapy/_compat.py`. It is twenty
lines and it means the rewrite is not a reason for anyone to stay on a broken release.

### Test offline

Every request goes through `httpx.MockTransport`. No token, no network, no rate limit,
so the suite runs in CI, in a fork, and on a laptop. A test suite that needs a secret is
a test suite contributors skip.
