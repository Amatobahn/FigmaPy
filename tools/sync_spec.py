"""Pull a new Figma OpenAPI spec release, regenerate, and report what changed.

    python tools/sync_spec.py --check          # is a newer spec out? exit 1 if yes
    python tools/sync_spec.py                  # sync to the latest release
    python tools/sync_spec.py --version 0.43.0 # sync to a specific release

Writes spec/openapi.yaml, spec/VERSION, the two generated modules, the version in
pyproject.toml, and a markdown report to docs/spec-changes.md. The report is what
goes in the pull request body, and its "Breaking" section is what decides whether a
human has to look before merging.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC_FILE = ROOT / "spec" / "openapi.yaml"
VERSION_FILE = ROOT / "spec" / "VERSION"
REPORT_FILE = ROOT / "docs" / "spec-changes.md"
PYPROJECT = ROOT / "pyproject.toml"

TAGS_URL = "https://api.github.com/repos/figma/rest-api-spec/tags"
SPEC_URL = "https://raw.githubusercontent.com/figma/rest-api-spec/v{version}/openapi/openapi.yaml"

HTTP_METHODS = ("get", "post", "put", "delete", "patch")


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "figmapy-spec-sync"})
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - fixed hosts
        return response.read()


def latest_version() -> str:
    tags = json.loads(fetch(TAGS_URL))
    versions = [t["name"].lstrip("v") for t in tags if re.fullmatch(r"v?\d+\.\d+\.\d+", t["name"])]
    if not versions:
        raise RuntimeError("No version tags found on figma/rest-api-spec")
    return max(versions, key=lambda v: tuple(int(p) for p in v.split(".")))


def current_version() -> str:
    return VERSION_FILE.read_text(encoding="utf8").strip()


# -- diffing ----------------------------------------------------------------


def _operations(spec: dict) -> dict:
    out = {}
    for path, methods in spec["paths"].items():
        for verb, op in methods.items():
            if verb not in HTTP_METHODS:
                continue
            params = op.get("parameters", [])
            body = op.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
            out[op["operationId"]] = {
                "route": f"{verb.upper()} {path}",
                "params": {p["name"] for p in params},
                "required_params": {p["name"] for p in params if p.get("required")},
                "body": set(body.get("properties", {})),
                "required_body": set(body.get("required", [])),
                "response": op.get("responses", {}).get("200", {}).get("$ref", ""),
            }
    return out


def _schemas(spec: dict) -> dict:
    out = {}
    for name, schema in spec["components"]["schemas"].items():
        parts = schema.get("allOf") or [schema]
        properties: set = set()
        required: set = set()
        for part in parts:
            properties |= set(part.get("properties", {}))
            required |= set(part.get("required", []))
        out[name] = {"properties": properties, "required": required}
    return out


def _bullets(title: str, items: list) -> list:
    return [f"### {title}", "", *(f"- {i}" for i in sorted(items)), ""] if items else []


def diff_report(old: dict, new: dict, old_version: str, new_version: str) -> tuple[str, bool]:
    """Markdown summary of the spec change, and whether anything in it is breaking."""
    old_ops, new_ops = _operations(old), _operations(new)
    old_schemas, new_schemas = _schemas(old), _schemas(new)

    added_ops = [f"`{new_ops[o]['route']}` ({o})" for o in new_ops.keys() - old_ops.keys()]
    removed_ops = [f"`{old_ops[o]['route']}` ({o})" for o in old_ops.keys() - new_ops.keys()]

    changed_ops, breaking_ops = [], []
    for name in old_ops.keys() & new_ops.keys():
        before, after = old_ops[name], new_ops[name]
        gone = (before["params"] - after["params"]) | (before["body"] - after["body"])
        fresh = (after["params"] - before["params"]) | (after["body"] - before["body"])
        newly_required = (after["required_params"] | after["required_body"]) - (
            before["required_params"] | before["required_body"]
        )
        if before["route"] != after["route"]:
            breaking_ops.append(f"`{name}` moved: `{before['route']}` -> `{after['route']}`")
        if gone:
            breaking_ops.append(f"`{name}` dropped parameters: {', '.join(sorted(gone))}")
        if newly_required:
            breaking_ops.append(f"`{name}` newly requires: {', '.join(sorted(newly_required))}")
        if fresh:
            changed_ops.append(f"`{name}` gained: {', '.join(sorted(fresh))}")

    added_schemas = sorted(new_schemas.keys() - old_schemas.keys())
    removed_schemas = sorted(old_schemas.keys() - new_schemas.keys())

    field_changes, breaking_fields = [], []
    for name in old_schemas.keys() & new_schemas.keys():
        before, after = old_schemas[name], new_schemas[name]
        gone = before["properties"] - after["properties"]
        fresh = after["properties"] - before["properties"]
        newly_required = after["required"] - before["required"] - fresh
        if gone:
            breaking_fields.append(f"`{name}` dropped fields: {', '.join(sorted(gone))}")
        if newly_required:
            breaking_fields.append(f"`{name}` newly requires: {', '.join(sorted(newly_required))}")
        if fresh:
            field_changes.append(f"`{name}` gained: {', '.join(sorted(fresh))}")

    breaking = breaking_ops + breaking_fields + [f"schema removed: `{s}`" for s in removed_schemas]

    lines = [
        f"# Figma spec {old_version} -> {new_version}",
        "",
        f"Generated by `tools/sync_spec.py` from "
        f"[figma/rest-api-spec@v{new_version}](https://github.com/figma/rest-api-spec/releases/tag/v{new_version}).",
        "",
        "| | count |",
        "| --- | --- |",
        f"| endpoints added | {len(added_ops)} |",
        f"| endpoints removed | {len(removed_ops)} |",
        f"| endpoints changed | {len(changed_ops)} |",
        f"| schemas added | {len(added_schemas)} |",
        f"| schemas removed | {len(removed_schemas)} |",
        f"| schemas with new fields | {len(field_changes)} |",
        f"| **breaking changes** | **{len(breaking)}** |",
        "",
    ]
    lines += _bullets("Breaking", breaking)
    lines += _bullets("New endpoints", added_ops)
    lines += _bullets("Removed endpoints", removed_ops)
    lines += _bullets("Changed endpoints", changed_ops)
    lines += _bullets("New schemas", added_schemas)
    lines += _bullets("New fields", field_changes)
    if not any([added_ops, removed_ops, changed_ops, added_schemas, field_changes, breaking]):
        lines += ["No functional change: descriptions or examples only.", ""]

    return "\n".join(lines), bool(breaking)


# -- applying ---------------------------------------------------------------


def set_project_version(version: str) -> None:
    text = PYPROJECT.read_text(encoding="utf8")
    updated = re.sub(r'^version = "[^"]+"', f'version = "{version}"', text, count=1, flags=re.M)
    if updated == text:
        raise RuntimeError("Could not find the version line in pyproject.toml")
    PYPROJECT.write_text(updated, encoding="utf8")


def sync(version: str) -> bool:
    """Download, regenerate and write the report. True if anything changed."""
    old_version = current_version()
    old_spec = yaml.safe_load(SPEC_FILE.read_text(encoding="utf8"))

    new_bytes = fetch(SPEC_URL.format(version=version))
    new_spec = yaml.safe_load(new_bytes.decode("utf8"))

    report, breaking = diff_report(old_spec, new_spec, old_version, version)

    SPEC_FILE.write_bytes(new_bytes)
    VERSION_FILE.write_text(f"{version}\n", encoding="utf8")
    set_project_version(version)
    subprocess.run([sys.executable, str(ROOT / "tools" / "generate.py")], check=True)

    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text(report + "\n", encoding="utf8")
    print(report)
    return breaking


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="only report whether a newer spec exists")
    parser.add_argument("--version", help="sync to this spec version instead of the latest")
    args = parser.parse_args()

    target = args.version or latest_version()
    current = current_version()

    if args.check:
        print(f"current={current} latest={target}")
        return 1 if target != current else 0

    if target == current:
        print(f"Already on Figma spec {current}, nothing to do.")
        return 0

    breaking = sync(target)
    print(f"\nSynced {current} -> {target}. Breaking changes: {'yes' if breaking else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
