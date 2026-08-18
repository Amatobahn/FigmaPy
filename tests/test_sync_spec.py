"""The spec diff decides whether a sync can be merged unattended, so it gets a test."""

from __future__ import annotations

import compileall
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))

import sync_spec  # noqa: E402


def spec(paths=None, schemas=None):
    return {"paths": paths or {}, "components": {"schemas": schemas or {}}}


def endpoint(operation_id, params=(), required=()):
    return {
        "operationId": operation_id,
        "parameters": [{"name": p, "required": p in required} for p in params],
        "responses": {},
    }


def report(old, new):
    return sync_spec.diff_report(old, new, "1.0.0", "1.1.0")


def test_no_change_is_not_breaking():
    one = spec({"/a": {"get": endpoint("getA")}})
    text, breaking = report(one, one)
    assert not breaking
    assert "No functional change" in text


def test_new_endpoint_is_additive():
    text, breaking = report(
        spec({"/a": {"get": endpoint("getA")}}),
        spec({"/a": {"get": endpoint("getA")}, "/b": {"get": endpoint("getB")}}),
    )
    assert not breaking
    assert "`GET /b` (getB)" in text


def test_new_optional_field_is_additive():
    text, breaking = report(
        spec(schemas={"Node": {"properties": {"id": {}}}}),
        spec(schemas={"Node": {"properties": {"id": {}, "tint": {}}}}),
    )
    assert not breaking
    assert "`Node` gained: tint" in text


@pytest.mark.parametrize(
    "old,new,expected",
    [
        (
            spec({"/a": {"get": endpoint("getA")}}),
            spec({"/b": {"get": endpoint("getA")}}),
            "moved",
        ),
        (
            spec({"/a": {"get": endpoint("getA", params=["depth"])}}),
            spec({"/a": {"get": endpoint("getA")}}),
            "dropped parameters: depth",
        ),
        (
            spec({"/a": {"get": endpoint("getA", params=["ids"])}}),
            spec({"/a": {"get": endpoint("getA", params=["ids"], required=["ids"])}}),
            "newly requires: ids",
        ),
        (
            spec(schemas={"Node": {"properties": {"id": {}, "old": {}}}}),
            spec(schemas={"Node": {"properties": {"id": {}}}}),
            "dropped fields: old",
        ),
        (
            spec(schemas={"Node": {"properties": {"id": {}}}}),
            spec(schemas={}),
            "schema removed: `Node`",
        ),
    ],
)
def test_removals_and_new_requirements_are_breaking(old, new, expected):
    text, breaking = report(old, new)
    assert breaking
    assert expected in text
    assert "### Breaking" in text


def test_allof_schemas_are_flattened():
    """Figma composes most node schemas with allOf, so both halves have to be seen."""
    text, breaking = report(
        spec(schemas={"Node": {"allOf": [{"properties": {"id": {}}}, {"properties": {"name": {}}}]}}),
        spec(schemas={"Node": {"allOf": [{"properties": {"id": {}}}]}}),
    )
    assert breaking
    assert "dropped fields: name" in text


def test_examples_compile():
    """They are documentation, but they are also the first thing anyone runs."""
    examples = pathlib.Path(__file__).resolve().parent.parent / "examples"
    assert compileall.compile_dir(str(examples), quiet=2, force=True)
