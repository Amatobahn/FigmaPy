# Versioning

## The rule

**The package version is the Figma spec version.**

`FigmaPy 0.42.0` is generated from [`figma/rest-api-spec`
v0.42.0](https://github.com/figma/rest-api-spec/releases/tag/v0.42.0). Nothing else.

```python
figmapy.__version__          # '0.42.0'
figmapy.FIGMA_SPEC_VERSION   # '0.42.0' - always the same string
```

`spec/VERSION` in the repository is the single source of truth. `tools/sync_spec.py`
writes it, writes the matching number into `pyproject.toml`, and a test fails if the two
ever disagree.

## Why not semver

Semver answers "will this upgrade break my code?". For a wrapper whose entire surface is
someone else's API, that question has a better answer: "which version of their API is
this?". Coupling the two numbers means:

- You can tell at a glance whether your installed version knows about a Figma feature.
  If Figma's changelog says a field landed in 0.44.0 and you have 0.42.0, you know.
- There is no judgement call in the release process, so a bot can run it. A human
  deciding "is this a minor or a patch?" is exactly the step that stalls, and stalling is
  what left the old PyPI release stranded on 2018.1.0 for seven years.
- Nobody has to maintain a mapping table between two version schemes.

The cost is that a FigmaPy version bump does not tell you whether *your* code breaks. The
pull request does: every spec sync ships with a generated diff, and anything removed or
newly required is labelled `breaking`. See [maintenance.md](maintenance.md).

## Fixes that are not spec changes

A bug in the hand-written parts — the client, retries, helpers, errors — ships as a PEP
440 post-release of whatever spec version is current:

```
0.42.0        spec v0.42.0
0.42.0.post1  same spec, a fix in figmapy/client.py
0.42.0.post2  same spec, another fix
0.43.0        spec v0.43.0, and everything in the posts above
```

`pip install FigmaPy==0.42.*` gets you the fixes without the spec moving under you.

## Pinning

| You want | Put this in your requirements |
| --- | --- |
| Whatever is newest | `FigmaPy` |
| A known-good spec version, plus fixes | `FigmaPy==0.42.*` |
| Byte-for-byte reproducible | `FigmaPy==0.42.0` |

Pinning is cheap here, because being behind is not a wall — see the escape hatches in the
[README](../README.md#nothing-here-should-ever-block-you). An old pin still talks to
today's Figma; it just has fewer typed conveniences for the newest fields.

## What counts as breaking

Decided mechanically by `tools/sync_spec.py`, not by taste:

- an endpoint disappeared, or moved to a different path
- a parameter or request-body field disappeared
- a parameter or field became required that was not
- a schema disappeared

Everything else — new endpoints, new optional parameters, new fields, description
changes — is additive. Additive syncs can merge and release without a human. Breaking
ones cannot.

## Zero major version

The package stays on `0.x` for as long as Figma's spec does. When Figma tags `1.0.0`, so
does this.
