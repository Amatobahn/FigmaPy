import figmapy
from unittest.mock import Mock


def test_get_file_images_from_nodes_sync():
    figma_session = figmapy.FigmaPy(token='test_token')
    figma_session.get_file_images = Mock(return_value=[])
    node = Mock()
    node.children = [node, node]
    node.id = 123
    figma_session.get_file_images_from_nodes_sync(nodes=[node, node])
