# Versioning

## The rule

**The package version is date-based: `YEAR.RELEASE.PATCH`.**

```
2026.1.0    first release of 2026
2026.1.1    patch fix within that release
2026.2.0    second release of 2026
2027.1.0    first release of 2027
```

This continues the scheme established by `FigmaPy 2018.1.0` on PyPI.

```python
figmapy.__version__          # '2026.1.0'
figmapy.FIGMA_SPEC_VERSION   # '0.42.0' - the Figma OpenAPI spec this was generated from
```

These two numbers are independent. `FIGMA_SPEC_VERSION` tells you which Figma spec
the client and models were generated from. `__version__` tells you the package release.

## Why date-based

- Continues the existing `2018.1.0` convention already on PyPI.
- `YEAR` gives an immediate sense of how recent the release is.
- No judgement call on major/minor/patch for what is essentially a generated wrapper —
  breaking changes are detected mechanically by `tools/sync_spec.py` and reported in the
  PR, not encoded in the version number.

## Figma spec updates

When the Figma spec is updated, `tools/sync_spec.py` bumps `spec/VERSION` and regenerates
`figmapy/_endpoints.py` and `figmapy/models.py`. The package version in `pyproject.toml`
is updated separately by the maintainer as part of the release.

```
spec/VERSION    0.42.0  -> 0.43.0    (written by sync_spec.py)
pyproject.toml  2026.1.0 -> 2026.2.0  (updated manually before tagging)
```

## Fixes that are not spec changes

A bug fix in the hand-written parts ships as a patch bump:

```
2026.1.0    initial release
2026.1.1    fix in figmapy/client.py
2026.2.0    next planned release (may include a new spec version)
```

## Pinning

| You want | Put this in your requirements |
| --- | --- |
| Whatever is newest | `FigmaPy` |
| A known-good release, plus patches | `FigmaPy==2026.1.*` |
| Byte-for-byte reproducible | `FigmaPy==2026.1.0` |

Pinning is cheap here, because being behind is not a wall: an old pin still talks to
today's Figma; it just has fewer typed conveniences for the newest fields. Use
`figma.request("GET", "/v1/...")` as an escape hatch for anything not yet wrapped.

## What counts as breaking

Decided mechanically by `tools/sync_spec.py`, not by taste:

- an endpoint disappeared, or moved to a different path
- a parameter or request-body field disappeared
- a parameter or field became required that was not
- a schema disappeared

Everything else — new endpoints, new optional parameters, new fields, description
changes — is additive. See [maintenance.md](maintenance.md).
