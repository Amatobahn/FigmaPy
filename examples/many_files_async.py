"""Fetch several files at once.

    python examples/many_files_async.py <url> <url> <url>

This is the case async is for. For one file, use figmapy.Figma -- the async client buys
nothing and costs you an event loop.
"""

import asyncio
import sys

import figmapy


async def main(urls):
    keys = [figmapy.file_key_from_url(u) for u in urls]
    async with figmapy.AsyncFigma() as figma:
        # depth=1 keeps the responses small: we only want the names here.
        files = await asyncio.gather(*(figma.get_file(k, depth=1) for k in keys))
    for key, file in zip(keys, files, strict=True):
        print(f"{key}  {file.name}  ({len(figmapy.pages(file))} pages)")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
