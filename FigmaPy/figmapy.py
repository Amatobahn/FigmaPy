import requests
import json
from .models import *


class FigmaPy:
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
                return json.loads(response.text)
            else:
                print(json.loads(response.text))
                return None
        except (requests.HTTPError, requests.exceptions.SSLError) as e:
            print('Error occurred attpempting to make an api request. {0}'.format(e))
            return None

    # -------------------------------------------------------------------------
    # OAUTH2
    # -------------------------------------------------------------------------
    """
    Create token from client_id, client_secret, code
    """
    def create_token(self, client_id, client_secret, redirect_uri, code):
        payload = {
            'client_id': '{0}'.format(client_id),
            'client_secret': '{0}'.format(client_secret),
            'grant_type': 'authorization_code',
            'redirect_uri': '{0}'.format(redirect_uri),
            'code': '{0}'.format(code)
        }
        try:
            response = requests.post(self.token_uri, data=payload)
            print(response.text)
            if response.status_code == 200:
                token_data = json.loads(response.text)
                return [token_data['access_token'], token_data['expires_in']]
            else:
                return None
        except requests.HTTPError:
            print('HTTP Error occurred while trying to generate access token.')
            return None

    """
    Returns API user's access token
    """
    def get_access_token(self):
        return self.api_token

    # -------------------------------------------------------------------------
    # SCOPE: FILES
    # -------------------------------------------------------------------------
    """
    Get the JSON file contents for a file.
    """
    def get_file(self, file_key, geometry=None, version=None):
        optional_data = ''
        if geometry is not None or version is not None:
            optional_data = '?'
            if geometry is not None:
                optional_data += str(geometry)
                if version is not None:
                    optional_data += '&{0}'.format(str(version))
            elif version is not None:
                optional_data += str(version)

        data = self.api_request('files/{0}{1}'.format(file_key, optional_data), method='get')
        return File(data['name'], data['document'], data['components'], data['lastModified'], data['thumbnailUrl'],
                    data['schemaVersion'], data['styles'])

    """
    Get the version history of a file.
    """
    def get_file_versions(self, file_key):
        data = self.api_request('files/{0}/versions'.format(file_key), method='get')
        return FileVersions(data['versions'], data['pagination'])

    """
    Get all comments on a file.
    """
    def get_comments(self, file_key):
        data = self.api_request('files/{0}/comments'.format(file_key), method='get')
        return Comments(data['comments'])

    """
    Create a comment on a file.
    """
    def post_comment(self, file_key, message, client_meta=None):
        payload = {'message': '{0}'.format(message)}
        if client_meta is not None:
            payload['client_meta'] = str(client_meta)
        data = self.api_request('files/{0}/comments{1}'.format(file_key, client_meta), method='post', payload=payload)
        return Comment(data['id'], data['file_key'], data['parent_id'], data['user'], data['created_at'],
                       data['resolved_at'], data['message'], data['client_meta'], data['order_id'])

    # -------------------------------------------------------------------------
    # SCOPE: IMAGES
    # -------------------------------------------------------------------------
    """
    Get urls for server-side rendered images from a file.
    """
    def get_file_images(self, file_key, ids, scale=None, format=None, version=None):
        optional_data = ''
        if scale is not None or format is not None or version is not None:
            if scale is not None:
                optional_data += '&{0}'.format(str(scale))
            if format is not None:
                optional_data += '&{0}'.format(str(format))
            if version is not None:
                optional_data += '&{0}'.format(str(version))
        id_array = []
        for id in ids:
            id_array.append(id)
        id_list = ','.join(id_array)
        data = self.api_request('images/{0}?ids={1}{2}'.format(file_key, id_list, optional_data), method='get')
        return FileImages(data['images'], data['err'])

    # -------------------------------------------------------------------------
    # SCOPE: TEAMS
    # -------------------------------------------------------------------------
    """
    Get all projects for a team
    """
    def get_team_projects(self, team_id):
        data = self.api_request('teams/{0}/projects'.format(team_id), method='get')
        return TeamProjects(data['projects'])

    # -------------------------------------------------------------------------
    # SCOPE: PROJECTS
    # -------------------------------------------------------------------------
    """
    Get all files for a project
    """
    def get_project_files(self, project_id):
        data = self.api_request('projects/{0}/files'.format(project_id))
        return ProjectFiles(data['files'])
