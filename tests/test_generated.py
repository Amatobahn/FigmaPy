"""Checks on the generated layer itself.

These are what make the weekly spec sync safe to merge: if regenerating from a new
spec drops an endpoint, breaks a signature, or leaves the checked-in files stale,
one of these fails.
"""

from __future__ import annotations

import inspect
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

import figmapy
from figmapy._endpoints import AsyncEndpoints, SyncEndpoints

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "openapi.yaml"
GENERATED = [ROOT / "figmapy" / "_endpoints.py", ROOT / "figmapy" / "models.py"]


def methods(cls) -> set:
    return {name for name, _ in inspect.getmembers(cls, inspect.isfunction)}


def spec_operations() -> set:
    spec = yaml.safe_load(SPEC.read_text(encoding="utf8"))
    from tools.generate import snake  # noqa: PLC0415 - test-only import

    return {
        snake(op["operationId"])
        for methods_ in spec["paths"].values()
        for verb, op in methods_.items()
        if verb in ("get", "post", "put", "delete", "patch")
    }


def test_every_spec_operation_has_a_method():
    assert spec_operations() == methods(SyncEndpoints)


def test_sync_and_async_have_the_same_surface():
    assert methods(SyncEndpoints) == methods(AsyncEndpoints)
    for name in methods(SyncEndpoints):
        sync = inspect.signature(getattr(SyncEndpoints, name))
        async_ = inspect.signature(getattr(AsyncEndpoints, name))
        assert sync == async_, name


def test_every_async_method_is_a_coroutine():
    for name in methods(AsyncEndpoints):
        assert inspect.iscoroutinefunction(getattr(AsyncEndpoints, name)), name


def test_package_version_matches_the_pinned_spec():
    pinned = (ROOT / "spec" / "VERSION").read_text(encoding="utf8").strip()
    assert figmapy.FIGMA_SPEC_VERSION == pinned
    # Package version is date-based (YEAR.RELEASE.PATCH), independent of spec version.
    assert re.match(r"^\d{4}\.\d+\.\d+", figmapy.__version__), figmapy.__version__


def test_models_accept_unknown_fields():
    node = figmapy.models.CanvasNode.model_validate(
        {
            "id": "0:1",
            "name": "Page 1",
            "type": "CANVAS",
            "scrollBehavior": "SCROLLS",
            "children": [],
            "backgroundColor": {"r": 0, "g": 0, "b": 0, "a": 1},
            "prototypeStartNodeID": None,
            "flowStartingPoints": [],
            "prototypeDevice": {"type": "NONE", "rotation": "NONE"},
            "aFieldFromTheFuture": "hello",
        }
    )
    assert node.aFieldFromTheFuture == "hello"


@pytest.mark.slow
def test_checked_in_code_matches_the_spec():
    """Fails if someone edited a generated file, or bumped the spec without regenerating."""
    before = {path: path.read_text(encoding="utf8") for path in GENERATED}
    try:
        subprocess.run([sys.executable, "tools/generate.py"], cwd=ROOT, check=True,
                       capture_output=True)
        for path, original in before.items():
            assert path.read_text(encoding="utf8") == original, (
                f"{path.name} is stale. Run: python tools/generate.py"
            )
    finally:
        for path, original in before.items():
            path.write_text(original, encoding="utf8")
