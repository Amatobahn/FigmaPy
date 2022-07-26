try:
    import aiohttp
except ImportError:
    print("Async dependencies have not been installed: [httpx]")

import requests
from FigmaPy.datatypes import File, Comment, FileMeta, Project
from FigmaPy.datatypes.results import (
    FileImages,
    FileVersions,
    Comments,
    TeamProjects,
) 

# fmt:off
class FigmaPyBase:
    def __init__(self, token, oauth2=False):
        self.api_uri = 'https://api.figma.com/v1/'
        self.token_uri = 'https://www.figma.com/oauth'
        self.api_token = token
        self.oauth2 = oauth2

    # -------------------------------------------------------------------------
    # FIGMA API
    # -------------------------------------------------------------------------
    '''
    Request Figma API
    '''
    def api_request(self, endpoint, method='get', payload=None):
        method = method.lower()

        if payload is None:
            payload = ''

        if self.oauth2:
            header = {'Authorization': 'Bearer {0}'.format(self.api_token)}
        else:
            header = {'X-Figma-Token': '{0}'.format(self.api_token)}

        header['Content-Type'] = 'application/json'

        try:
            if method == 'head':
                response = requests.head('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method == 'delete':
                response = requests.delete('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method == 'get':
                response = requests.get('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            elif method == 'options':
                response = requests.options('{0}{1}'.format(self.api_uri, endpoint), headers=header)
            elif method == 'post':
                response = requests.post('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            elif method == 'put':
                response = requests.put('{0}{1}'.format(self.api_uri, endpoint), headers=header, data=payload)
            else:
                response = None
            
            if response.status_code == 200:
                return response.json()
            else:
                return None

        except (Exception, requests.HTTPError, requests.exceptions.SSLError) as e:
            print('Error occurred attempting to make an api request. {0}'.format(e))
            return None

# fmt:on
    # -------------------------------------------------------------------------
    # SCOPE: FILES
    # -------------------------------------------------------------------------

    def _build_get_file_url(self, file_key, geometry=None, version=None, parent=None):
        # https://www.figma.com/developers/api#get-files-endpoint
        """
        Build API URL from Parameters
        """
        optional_data = ''
        if geometry is not None or version is not None:
            optional_data = '?'
            if geometry is not None:
                optional_data += str(geometry)
                if version is not None:
                    optional_data += '&{0}'.format(str(version))
            elif version is not None:
                optional_data += str(version)
         
        return 'files/{0}{1}'.format(file_key, optional_data)

    def get_file(self, file_key, geometry=None, version=None, parent=None):
        # https://www.figma.com/developers/api#get-files-endpoint
        """
        Get the JSON file contents for a file.
        """
        api_url = self._build_get_file_url(file_key, geometry, version, parent) 
        data = self.api_request(api_url, method='get')
        # return data
        if data is not None:
            return File(data['name'], data['document'], data['components'], data['lastModified'], data['thumbnailUrl'],
                        data['schemaVersion'], data['styles'], file_key=file_key, pythonParent=parent)

    
    def _build_get_file_nodes_url(self, file_key, ids, version=None, depth=None, geometry=None, plugin_data=None):
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
        
        return 'files/{0}/nodes?ids={1}{2}'.format(file_key,id_list, optional_data)

    def get_file_nodes(self, file_key, ids, version=None, depth=None, geometry=None, plugin_data=None):
        # https://www.figma.com/developers/api#get-file-nodes-endpoint
        api_url = self._build_get_file_nodes_url(file_key, ids, version=None, depth=None, geometry=None, plugin_data=None)
        data = self.api_request(api_url, method='get')
        return data
    
    def _build_get_file_images_url(self, file_key, ids, scale=None, format=None, version=None):
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

    def get_file_images(self, file_key, ids, scale=None, format=None, version=None):
        # https://www.figma.com/developers/api#get-images-endpoint
        """
        Get urls for server-side rendered images from a file.
        If the node is not an image, a rasterized version of the node will be returned.
        """
        api_url = self._build_get_file_images_url(file_key, ids, scale=None, format=None, version=None)
        data = self.api_request(api_url, method='get')
        if data is not None:
            return FileImages(data['images'], data['err'])


class AioHttpFigmaPy(FigmaPyBase):
    """
    Async version of the FigmaPy backend
    """
    def __init__(self, client=aiohttp.ClientSession(), *args, **kwargs):
        """
        client (optional): An asynchronous web session/client. Defaults to aiohttp.ClientSession().
                Can be custom Python object that exposes methods for all HTTP verbs.
        """
        self.client = client 
        super().__init__(*args, **kwargs)
    
    async def async_api_request(self, endpoint, method='get', payload=''):
        # Make async web requests

        DATA_METHODS = ('post', 'put', 'patch')
        method = method.lower()
        if self.oauth2:
            header = {'Authorization': 'Bearer {0}'.format(self.api_token)}
        else:
            header = {'X-Figma-Token': '{0}'.format(self.api_token)}

        header['Content-Type'] = 'application/json'
        url = '{0}{1}'.format(self.api_uri, endpoint)
        try:
            request_func = getattr(self.client, method)
        except AttributeError as e:
            print('Unsupported HTTP request, could be as a result of an invalid method {0}'.format(e))
        
        try:        
            # Check if we need to pass data as a param
            if method in DATA_METHODS:
                response = await request_func(url, headers=header, data=payload)
            else:
                response = await request_func(url, headers=header)    
            # Return data
            return await response.json()

        except Exception as e:
            print('Error occurred attempting to make an API request. {0}'.format(e))
            return None 
            
    async def get_file(self, file_key, geometry=None, version=None, parent=None):
        # https://www.figma.com/developers/api#get-files-endpoint
        
        api_url = self._build_get_file_url(file_key, geometry, version, parent) 
        data = await self.async_api_request(api_url, method='get')
        if data is not None:
            return File(data['name'], data['document'], data['components'], data['lastModified'], data['thumbnailUrl'],
                        data['schemaVersion'], data['styles'], file_key=file_key, pythonParent=parent)

    async def get_file_nodes(self, file_key, ids, version=None, depth=None, geometry=None, plugin_data=None):
        # https://www.figma.com/developers/api#get-file-nodes-endpoint
    
        api_url = self._build_get_file_nodes_url(file_key, ids, version=None, depth=None, geometry=None, plugin_data=None)
        data = await self.async_api_request(api_url, method='get')
        return data
    
    async def get_file_images(self, file_key, ids, scale=None, format=None, version=None):
        # https://www.figma.com/developers/api#get-images-endpoint
    
        api_url = self._build_get_file_images_url(file_key, ids, scale=None, format=None, version=None)
        data = await self.async_api_request(api_url, method='get')
        if data is not None:
            return FileImages(data['images'], data['err'])