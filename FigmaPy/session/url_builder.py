
class FigmaPyBase:
    def __init__(self, token, oauth2=False):
        self.api_uri = 'https://api.figma.com/v1/'
        self.token_uri = 'https://www.figma.com/oauth'
        self.api_token = token
        self.oauth2 = oauth2

    @staticmethod
    def _build_get_file_url(file_key, geometry=None, version=None, plugin_data=None):
        # https://www.figma.com/developers/api#get-files-endpoint
        """
        Build API URL from Parameters
        """
        optional_data = ''
        if geometry or version or plugin_data:
            optional_data = '?'
            if geometry is not None:
                optional_data += f'geometry={geometry}'

            if optional_data != '?':
                optional_data += '&'
            if version is not None:
                optional_data += f'version={version}'

            if optional_data != '?':
                optional_data += '&'
            if plugin_data is not None:
                optional_data += f'plugin_data={plugin_data}'

        return 'files/{0}{1}'.format(file_key, optional_data)

    @staticmethod
    def _build_get_file_nodes_url(file_key, ids, version=None, depth=None, geometry=None, plugin_data=None):
        # https://www.figma.com/developers/api#get-file-nodes-endpoint
        """
        Build API URL from Parameters
        """
        optional_data = ''
        if depth:
            optional_data += f'&depth={depth}'
        if version:
            optional_data += f'&version={version}'
        if geometry:
            optional_data += f'&geometry={geometry}'
        if plugin_data:
            optional_data += f'&plugin_data={plugin_data}'

        id_array = []
        for id in ids:
            id_array.append(id)
        id_list = ','.join(id_array)

        return 'files/{0}/nodes?ids={1}{2}'.format(file_key, id_list, optional_data)

    @staticmethod
    def _build_get_file_images_url(file_key, ids, scale=None, format=None, version=None):
        optional_data = ''
        if scale is not None or format is not None or version is not None:
            if scale is not None:
                optional_data += '&scale={0}'.format(str(scale))
            if format is not None:
                optional_data += '&format={0}'.format(str(format))
            if version is not None:
                optional_data += '&version={0}'.format(str(version))
        id_array = []
        for id in ids:
            id_array.append(id)
        id_list = ','.join(id_array)
        return 'images/{0}?ids={1}{2}'.format(file_key, id_list, optional_data)
