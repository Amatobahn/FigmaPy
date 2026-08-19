from __future__ import annotations

import httpx
import pytest

import figmapy

TOKEN = "figd_test"


def canvas(node_id: str, name: str, children: list | None = None) -> dict:
    return {
        "id": node_id,
        "name": name,
        "type": "CANVAS",
        "scrollBehavior": "SCROLLS",
        "children": children or [],
        "backgroundColor": {"r": 0.1, "g": 0.1, "b": 0.1, "a": 1.0},
        "prototypeStartNodeID": None,
        "flowStartingPoints": [],
        "prototypeDevice": {"type": "NONE", "rotation": "NONE"},
    }


def text(node_id: str, name: str, characters: str) -> dict:
    return {
        "id": node_id,
        "name": name,
        "type": "TEXT",
        "scrollBehavior": "SCROLLS",
        "characters": characters,
        "blendMode": "PASS_THROUGH",
        "absoluteBoundingBox": {"x": 0, "y": 0, "width": 10, "height": 10},
        "absoluteRenderBounds": {"x": 0, "y": 0, "width": 10, "height": 10},
        "constraints": {"vertical": "TOP", "horizontal": "LEFT"},
        "style": {},
        "characterStyleOverrides": [],
        "styleOverrideTable": {},
        "lineTypes": [],
        "lineIndentations": [],
        "fills": [],
        "effects": [],
    }


@pytest.fixture
def file_payload() -> dict:
    """A realistic GET /v1/files/{key} body, trimmed to what the spec requires."""
    return {
        "name": "Untitled",
        "role": "owner",
        "lastModified": "2026-08-19T23:01:51Z",
        "editorType": "figma",
        "thumbnailUrl": "https://example.invalid/thumb.png",
        "version": "2239202519",
        "schemaVersion": 0,
        "components": {},
        "componentSets": {},
        "styles": {},
        "document": {
            "id": "0:0",
            "name": "Document",
            "type": "DOCUMENT",
            "scrollBehavior": "SCROLLS",
            "children": [
                canvas("0:1", "Page 1", [text("1:2", "Title", "Hello")]),
                canvas("0:2", "Page 2"),
            ],
        },
    }


@pytest.fixture
def make_client():
    """Build a Figma client whose transport is a callable you control.

    handler(request) -> httpx.Response
    """
    created = []

    def factory(handler, **kwargs):
        transport = httpx.MockTransport(handler)
        client = figmapy.Figma(
            TOKEN, http_client=httpx.Client(transport=transport), **kwargs
        )
        created.append(client)
        return client

    yield factory
    for client in created:
        client.http.close()
