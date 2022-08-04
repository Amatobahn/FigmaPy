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
from . import url_builder
from .base import FigmaPyBase


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
            
    async def get_file(self, key, geometry=None, version=None, parent=None):
        # https://www.figma.com/developers/api#get-files-endpoint
        
        api_url = url_builder.get_file(key, geometry, version, parent)
        data = await self.async_api_request(api_url, method='get')
        if data is not None:
            # insert python helper attributes
            data['mainFileKey'] = key
            data['_parent'] = parent
            return File(**data)

    async def get_file_nodes(self, file_key, ids, version=None, depth=None, geometry=None, plugin_data=None):
        # https://www.figma.com/developers/api#get-file-nodes-endpoint
    
        api_url = url_builder.get_file_nodes(file_key, ids, version=None, depth=None, geometry=None, plugin_data=None)
        data = await self.async_api_request(api_url, method='get')
        return data
    
    async def get_file_images(self, file_key, ids, scale=None, format=None, version=None):
        # https://www.figma.com/developers/api#get-images-endpoint
    
        api_url = url_builder.get_file_images(file_key, ids, scale=None, format=None, version=None)
        data = await self.async_api_request(api_url, method='get')
        if data is not None:
            return FileImages(data['images'], data['err'])
