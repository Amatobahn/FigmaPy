"""Print the node tree of a Figma file, then every text string in it.

    python examples/inspect_file.py https://www.figma.com/design/aBc123XyZ/My-File
"""

import sys

import figmapy


def main(url):
    figma = figmapy.Figma()  # reads FIGMA_TOKEN
    key = figmapy.file_key_from_url(url)
    file = figma.get_file(key)

    print(f"{file.name}  (last modified {file.lastModified})\n")
    for page in figmapy.pages(file):
        print(page.name)
        for node in figmapy.walk(page):
            print(f"  {node.type:<16} {node.name}")

    print("\nText:")
    for text in figmapy.find_all(file.document, type="TEXT"):
        print(f"  {text.characters!r}")


if __name__ == "__main__":
    main(sys.argv[1])
