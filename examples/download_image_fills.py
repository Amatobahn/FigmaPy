"""Download the bitmaps used as image fills in a file.

    python examples/download_image_fills.py https://www.figma.com/design/aBc123XyZ/My-File out/

These are the source images, not renders of nodes. For renders, see
export_components.py. The URLs expire, so download them now rather than storing them.
"""

import sys
from pathlib import Path

import httpx

import figmapy


def main(url, out_dir="."):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    figma = figmapy.Figma()
    fills = figma.get_image_fills(figmapy.file_key_from_url(url))

    for image_ref, image_url in fills.meta.images.items():
        response = httpx.get(image_url, follow_redirects=True)
        suffix = {"image/png": ".png", "image/jpeg": ".jpg", "image/svg+xml": ".svg"}.get(
            response.headers.get("content-type", "").split(";")[0], ""
        )
        path = out / f"{image_ref}{suffix}"
        path.write_bytes(response.content)
        print(path)


if __name__ == "__main__":
    main(*sys.argv[1:])
