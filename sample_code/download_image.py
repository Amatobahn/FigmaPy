import figmapy
from pathlib import Path
import requests


# TODO clean up this sample, to much noise, quite hacky

object_path = Path("/Game/ui_textures")
file_location = Path(r'C:\downloads')
file_key = 'REDACTED'
auth_key = 'REDACTED'

# # ------- get file content, nodes -----------
figmaPy = figmapy.FigmaPy(auth_key)
file = figmaPy.get_file(file_key)
page1 = file.document.children[0]
nodes = page1.get_children_recursively()

# # -------- write json file to disk, for testing --------
# import json
# with open(r"C:\repos\figma notes\flow-sample.json", 'w') as outfile:
#     json.dump(file, outfile,  indent=4)
# # -------------------------------------------------------


file_images = figmaPy.get_file_images(file_key, ids=[node.id for node in nodes], scale=1, format='svg')
print(file_images)

i = 0
for id, img_url in file_images.images.items():
    node = nodes[i]
    image_rq = requests.get(img_url)

    # we check the export settings from the node, if they exist, we use the format from the node
    # note this won't work well since we hardcoded file_images to svg in the previous lines
    # we don't have to use export settings
    export_type = 'svg'
    if node.exportSettings:
        for settings in node.exportSettings:
            export_type = settings.format.lower()

    file_name = node.name + '.' + export_type
    with open(str(file_location / file_name), 'wb') as handler:
        handler.write(image_rq.content)

    # break  # only get the first image to speed up testing
    i += 1
