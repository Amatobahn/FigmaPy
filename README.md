![alt text](http://www.iamgregamato.com/img/fp_logo.svg)
<p align=center>
  <a href="https://badge.fury.io/py/FigmaPy">
    <img src="https://badge.fury.io/py/FigmaPy.svg" alt="PyPI version" height="18">
  </a>
</p>

An unofficial Python3+ wrapper for Figma API

### Quick start

```python
import FigmaPy
import pprint

token = 'REPLACE_WITH_YOUR_TOKEN'  # can be found in your figma user profile page
file_key = 'REPLACE_WITH_YOUR_FILE_KEY'  # can be found in the URL of the file
figmaPy = FigmaPy.FigmaPy(token=token)
file = figmaPy.get_file(file_key=file_key)

print([x.name for x in file.document.children])
# ['Page 1', 'Page 2']

page1 = file.document.children[0]
print([x.name for x in page1.children])
# ['myArrow', 'myGroup', 'myImage']

ids = [x.id for x in page1.children]
print(ids)
# ['7:2', '7:6', '21:4']

images = figmaPy.get_file_images(file_key=file_key, ids=ids)
pprint.pprint(images.images)
# {'21:4': 'https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/9bc9fdbd-REDACTED-2d1f31e9b57e',
#  '7:2': 'https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/de2afe63d-REDACTED-8abc-9ca5b5f88ac8',
#  '7:6': 'https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/f56d5d8dd-REDACTED-af17-461010e0af14'}
```

### Install 
From PyPI:
```bash
pip install FigmaPy
```
Using Distributed Wheel from GitHub:
```bash
pip install FigmaPy-2018.1.0-py3-none-any.whl
```
API Documentation : https://www.figma.com/developers/docs
