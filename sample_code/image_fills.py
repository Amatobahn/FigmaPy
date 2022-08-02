import FigmaPy
from pprint import pprint
import requests
from pathlib import Path

file_key = 'REDACTED'
auth_key = 'REDACTED'
file_location = Path(r'C:\downloads\image_fills')

figmaPy = FigmaPy.FigmaPy(auth_key)
file = figmaPy.get_file(file_key)
page1 = file.document.children[0]
nodes = page1.get_children_recursively()

data = figmaPy.get_image_fills(file_key)

pprint(data)
# {'error': False,
#  'i18n' : None,
#  'meta' : {'images': {'REDACTED': 'https://s3-alpha-sig.figma.com/img/4be7/36e4/REDACTED?Expires=165892800&Signature=REDACTED__&Key-Pair-Id=REDACTED',
#                       'REDACTED': 'https://s3-alpha-sig.figma.com/img/4be7/36e4/REDACTED?Expires=165892800&Signature=REDACTED__&Key-Pair-Id=REDACTED'}},
#  'status': 200}

for id, img_url in data['meta']['images'].items():
    print(id)
    print(img_url)

    # download image
    image_rq = requests.get(img_url)
    file_name = str(id).replace(':', '_') + '.' + 'svg'
    with open(str(file_location/file_name), 'wb') as handler:
        handler.write(image_rq.content)
