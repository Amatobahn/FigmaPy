from figmapy.session import current


class FigmaPyBase:
    def __init__(self, token, oauth2=False):
        current.figma_session = self
        self.api_uri = 'https://api.figma.com/v1/'
        self.token_uri = 'https://www.figma.com/oauth'
        self.api_token = token
        self.oauth2 = oauth2

    # shared functions between sync and async, used by figma datatypes
    def get_file_images_sync(self, *args, **kwargs):
        raise NotImplementedError

    def get_file_images_from_nodes_sync(self, nodes, *args, **kwargs):
        if not nodes:
            return []
        file_key = nodes[0].get_file_key()
        node_ids = [node.id for node in nodes]
        return self.get_file_images_sync(file_key=file_key, ids=node_ids, *args, **kwargs)
