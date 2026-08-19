"""Download every component in a file as SVG.

    python examples/export_components.py https://www.figma.com/design/aBc123XyZ/My-File out/

Renders the whole batch in one request. Asking Figma to render nodes one at a time is
the fastest way to get rate limited.
"""

import re
import sys
from pathlib import Path

import httpx

import figmapy


def safe_filename(name):
    return re.sub(r"[^\w.-]+", "_", name).strip("_") or "unnamed"


def main(url, out_dir="."):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    figma = figmapy.Figma()
    key = figmapy.file_key_from_url(url)
    file = figma.get_file(key)

    components = figmapy.find_all(file.document, type="COMPONENT")
    print(f"{len(components)} components")
    if not components:
        return

    urls = figmapy.image_urls(figma, key, components, format="svg")
    by_id = {node.id: node for node in components}

    for node_id, image_url in urls.items():
        if not image_url:
            print(f"  render failed: {by_id[node_id].name}")
            continue
        path = out / f"{safe_filename(by_id[node_id].name)}.svg"
        path.write_bytes(httpx.get(image_url).content)
        print(f"  {path}")


if __name__ == "__main__":
    main(*sys.argv[1:])
