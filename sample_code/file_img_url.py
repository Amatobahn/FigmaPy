import FigmaPy
import FigmaPy.utils

file_key = "REDACTED"
auth_key = "REDACTED"

# # ------- get file content, nodes -----------
figmaPy = FigmaPy.FigmaPy(auth_key)
file = figmaPy.get_file(file_key)
page1 = file.document.children[0]
nodes = page1.get_children_recursively()

# # ------ testing the new node get img url function ------
for node in nodes:
    print(type(node))
    print("imageRef:", node.fills[0].imageRef)
    print("get_file_key:", FigmaPy.utils.get_file_key(node))
    print("get_file_image_url:", node.fills[0].get_file_image_url())
    # TODO: fix this
    #  file_images = root_parent.get_file_images(file_key=self.get_file_key(),
    #  AttributeError: 'NoneType' object has no attribute 'get_file_images'
    print("get_file_image_url node:", node.get_file_image_url())
    print("-----------------")
