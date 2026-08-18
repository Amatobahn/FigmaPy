"""List the comments on a file, post one, then delete it again.

    python examples/comments.py https://www.figma.com/design/aBc123XyZ/My-File
"""

import sys

import figmapy


def main(url):
    figma = figmapy.Figma()
    key = figmapy.file_key_from_url(url)

    for comment in figma.get_comments(key).comments:
        print(f"{comment.user.handle}: {comment.message}")

    posted = figma.post_comment(key, message="posted by figmapy")
    print(f"\nposted {posted.id}")

    figma.delete_comment(key, posted.id)
    print(f"deleted {posted.id}")


if __name__ == "__main__":
    main(sys.argv[1])
