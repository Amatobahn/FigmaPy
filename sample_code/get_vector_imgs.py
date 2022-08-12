import FigmaPy

file_key = "REDACTED"
auth_key = "REDACTED"

figmaPy = FigmaPy.FigmaPy(auth_key)
file = figmaPy.get_file(file_key)
page1 = file.document.children[0]
nodes = page1.get_children_recursively()

urls = figmaPy.get_vector_images(file_key=file_key, nodes=nodes)
print("urls:", urls)
