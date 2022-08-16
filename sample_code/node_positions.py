import figmapy

file_key = 'REDACTED'
auth_key = 'REDACTED'

figmaPy = figmapy.FigmaPy(auth_key)
file = figmaPy.get_file(file_key)
page1 = file.document.children[0]
nodes = page1.get_children_recursively()
node_positions = [node.absoluteBoundingBox for node in nodes]
print([(pos.x, pos.y) for pos in node_positions])
# [(24.0, -233.0), (-890.0, -110.0), (-890.0, -213.0), (-852.0, -317.0), (-890.0, -7.0), (-890.0, 85.0), (478.0, -65.0)]
