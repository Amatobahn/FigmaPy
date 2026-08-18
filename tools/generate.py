"""Generate figmapy/models.py and figmapy/_endpoints.py from spec/openapi.yaml.

Run: python tools/generate.py

Everything this writes is machine-generated and must never be hand-edited.
Hand-written behaviour lives in figmapy/client.py, helpers.py and _compat.py.
"""

from __future__ import annotations

import keyword
import re
import subprocess
import sys
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "openapi.yaml"
MODELS_OUT = ROOT / "figmapy" / "models.py"
ENDPOINTS_OUT = ROOT / "figmapy" / "_endpoints.py"

HTTP_METHODS = ("get", "post", "put", "delete", "patch")

TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "list",
    "object": "dict",
}


def snake(name: str) -> str:
    """getFileNodes -> get_file_nodes"""
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def safe(name: str) -> str:
    return name + "_" if keyword.iskeyword(name) else name


def py_type(schema: dict, spec: dict) -> str:
    """Python hint for a parameter schema. Scalar $refs are followed, objects stay Any."""
    seen = set()
    while schema and "$ref" in schema:
        ref = schema["$ref"]
        if ref in seen:
            return "Any"
        seen.add(ref)
        schema = spec["components"]["schemas"].get(ref.rsplit("/", 1)[-1], {})
    if not schema:
        return "Any"
    return TYPE_MAP.get(schema.get("type"), "Any")


def response_models(spec: dict) -> dict:
    """Map each components/responses entry to the model class that will represent it.

    A response whose body is a bare $ref reuses the referenced model, so `post_comment`
    returns `Comment` rather than a `PostCommentResponse` wrapper. Everything else gets
    a class of its own, named after the response.
    """
    mapping = {}
    for name, response in spec["components"].get("responses", {}).items():
        schema = response.get("content", {}).get("application/json", {}).get("schema")
        if schema is None:
            continue
        if list(schema) == ["$ref"]:
            mapping[name] = schema["$ref"].rsplit("/", 1)[-1]
        else:
            mapping[name] = name
    return mapping


def hoist_responses(spec: dict) -> dict:
    """Copy response bodies into components/schemas so models get generated for them.

    datamodel-code-generator only emits classes for components/schemas, and the Figma
    spec keeps every endpoint's response body under components/responses.
    """
    schemas = spec["components"]["schemas"]
    for name, model in response_models(spec).items():
        if model != name or name in schemas:
            continue  # bare $ref, or a name that already exists as a schema
        schema = spec["components"]["responses"][name]["content"]["application/json"]["schema"]
        schemas[name] = dict(schema, description=spec["components"]["responses"][name].get("description", ""))
    return spec


def generate_models(flat_spec_path: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        "datamodel_code_generator",
        "--input", str(flat_spec_path),
        "--input-file-type", "openapi",
        "--output", str(MODELS_OUT),
        "--output-model-type", "pydantic_v2.BaseModel",
        "--base-class", "figmapy._base.FigmaModel",
        "--target-python-version", "3.10",
        "--no-use-union-operator",
        "--use-annotated",
        "--use-schema-description",
        "--collapse-root-models",
        "--disable-timestamp",
        "--formatters", "black",
    ]
    subprocess.run(cmd, check=True)
    # RootModel is generated as a bare pydantic RootModel; it does not inherit our base
    # class, which is fine -- root models hold a single value and have no extra fields.
    text = MODELS_OUT.read_text(encoding="utf8")
    # pydantic maps `format: uri` to AnyUrl, which normalises the URL and is not a str.
    # Figma hands out signed, short-lived URLs; give them back exactly as received.
    text = _urls_as_str(text)
    MODELS_OUT.write_text(
        '"""Generated from spec/openapi.yaml by tools/generate.py. Do not edit."""\n\n'
        "# fmt: off\n"
        "# flake8: noqa\n" + text,
        encoding="utf8",
    )


def _urls_as_str(text: str) -> str:
    """Swap pydantic's AnyUrl for plain str throughout the generated models.

    pydantic maps `format: uri` to AnyUrl, which normalises what it parses (adding a
    trailing slash, among other things) and is not a str, so `url.startswith(...)`
    blows up. Figma hands out signed, short-lived URLs; give them back untouched.
    """
    out = []
    for line in text.splitlines(keepends=True):
        if line.startswith("from pydantic import"):
            head, _, names = line.partition("import")
            kept = [n for n in names.split(",") if n.strip() != "AnyUrl"]
            line = f"{head}import{','.join(kept)}"
        else:
            line = line.replace("AnyUrl", "str")
        out.append(line)
    return "".join(out)


class Operation:
    def __init__(self, path: str, method: str, op: dict, spec: dict):
        self.path = path
        self.method = method.upper()
        self.op = op
        self.spec = spec
        self.name = snake(op["operationId"])
        self.summary = op.get("summary", "")
        self.description = op.get("description", "")

        params = op.get("parameters", [])
        self.path_params = [p for p in params if p["in"] == "path"]
        self.query_params = [p for p in params if p["in"] == "query"]

        body = op.get("requestBody")
        self.body_props: list[tuple[str, dict, bool]] = []
        if body:
            schema = body["content"]["application/json"]["schema"]
            required = set(schema.get("required", []))
            for prop, prop_schema in schema.get("properties", {}).items():
                self.body_props.append((prop, prop_schema, prop in required))

        ref = op.get("responses", {}).get("200", {}).get("$ref", "")
        response_name = ref.rsplit("/", 1)[-1] if ref else None
        self.response_model = response_models(spec).get(response_name) if response_name else None

    def signature(self, is_async: bool) -> str:
        args = ["self"]
        for p in self.path_params:
            args.append(f"{safe(p['name'])}: {py_type(p['schema'], self.spec)}")

        kwargs = []
        for p in self.query_params:
            hint = py_type(p["schema"], self.spec)
            if p.get("required"):
                kwargs.append(f"{safe(p['name'])}: {hint}")
            else:
                kwargs.append(f"{safe(p['name'])}: Optional[{hint}] = None")
        for prop, prop_schema, required in self.body_props:
            hint = py_type(prop_schema, self.spec)
            if required:
                kwargs.append(f"{safe(prop)}: {hint}")
            else:
                kwargs.append(f"{safe(prop)}: Optional[{hint}] = None")

        if kwargs:
            args.append("*")
            args.extend(kwargs)

        ret = f'"models.{self.response_model}"' if self.response_model else "Any"
        prefix = "async def" if is_async else "def"
        joined = ",\n        ".join(args)
        return f"    {prefix} {self.name}(\n        {joined},\n    ) -> Union[{ret}, dict]:"

    def docstring(self) -> str:
        lines = [self.summary or self.name]
        if self.description:
            lines.append("")
            body = self.description.strip()
            # keep it readable in a terminal without dragging in the whole markdown blob
            if len(body) > 700:
                body = body[:700].rsplit("\n", 1)[0] + "\n..."
            lines.extend(body.splitlines())
        lines.append("")
        lines.append(f"{self.method} {self.path}")
        text = "\n".join(lines)
        return textwrap.indent(f'"""{text}\n"""', "        ")

    def call(self, is_async: bool) -> str:
        path_expr = repr(self.path)
        if self.path_params:
            fmt = ", ".join(f"{p['name']}={safe(p['name'])}" for p in self.path_params)
            path_expr = f"{path_expr}.format({fmt})"

        params = (
            "{" + ", ".join(f"{p['name']!r}: {safe(p['name'])}" for p in self.query_params) + "}"
            if self.query_params
            else "None"
        )
        json_body = (
            "{" + ", ".join(f"{p!r}: {safe(p)}" for p, _, _ in self.body_props) + "}"
            if self.body_props
            else "None"
        )
        model = f"models.{self.response_model}" if self.response_model else "None"
        await_ = "await " if is_async else ""
        return (
            f"        return {await_}self._call(\n"
            f"            {self.method!r},\n"
            f"            {path_expr},\n"
            f"            params={params},\n"
            f"            json_body={json_body},\n"
            f"            model={model},\n"
            f"        )"
        )

    def render(self, is_async: bool) -> str:
        return "\n".join([self.signature(is_async), self.docstring(), self.call(is_async), ""])




HEADER = '''"""Generated from spec/openapi.yaml by tools/generate.py. Do not edit.

One method per Figma REST API operation, for both the sync and async clients.
`_call` is implemented by figmapy.client.
"""

# fmt: off
# flake8: noqa

from __future__ import annotations

from typing import Any, Optional, Union

from . import models

FIGMA_SPEC_VERSION = "{spec_version}"


'''


def generate_endpoints(spec: dict, spec_version: str) -> int:
    operations = [
        Operation(path, method, op, spec)
        for path, methods in spec["paths"].items()
        for method, op in methods.items()
        if method in HTTP_METHODS
    ]
    operations.sort(key=lambda o: o.name)

    out = [HEADER.format(spec_version=spec_version)]
    for is_async, cls in ((False, "SyncEndpoints"), (True, "AsyncEndpoints")):
        out.append(f"class {cls}:\n")
        for op in operations:
            out.append(op.render(is_async))
            out.append("")
        out.append("\n")

    ENDPOINTS_OUT.write_text("\n".join(out).rstrip() + "\n", encoding="utf8")
    return len(operations)


def main() -> None:
    spec = yaml.safe_load(SPEC.read_text(encoding="utf8"))
    spec_version = (ROOT / "spec" / "VERSION").read_text(encoding="utf8").strip()

    count = generate_endpoints(spec, spec_version)
    print(f"wrote {ENDPOINTS_OUT.relative_to(ROOT)} ({count} operations)")

    flat = ROOT / "spec" / ".openapi.flat.yaml"
    yaml.safe_dump(hoist_responses(spec), flat.open("w", encoding="utf8"), sort_keys=False)
    try:
        generate_models(flat)
    finally:
        flat.unlink(missing_ok=True)
    classes = MODELS_OUT.read_text(encoding="utf8").count("\nclass ")
    print(f"wrote {MODELS_OUT.relative_to(ROOT)} ({classes} models)")


if __name__ == "__main__":
    main()
