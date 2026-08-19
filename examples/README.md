# Examples

Runnable scripts. Each one needs a Figma personal access token:

```
export FIGMA_TOKEN=figd_...          # Windows: set FIGMA_TOKEN=figd_...
python examples/export_components.py https://www.figma.com/design/aBc123XyZ/My-File
```

| Script | What it does |
| --- | --- |
| `inspect_file.py` | Print the node tree of a file, and every text string in it |
| `export_components.py` | Download every component in a file as SVG |
| `download_image_fills.py` | Download the bitmaps used as image fills |
| `comments.py` | List comments, post one, delete it |
| `many_files_async.py` | Fetch a list of files concurrently with `AsyncFigma` |
| `not_wrapped_yet.py` | Call an endpoint this version has no method for |
