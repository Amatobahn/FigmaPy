import requests
import json
from FigmaPy.datatypes import File, Comment, FileMeta, Project
from FigmaPy.datatypes.results import FileImages, FileVersions, Comments, TeamProjects#, ProjectFiles


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
                return json.loads(response.text)
            else:
                print(response.text)
                return None
        except (Exception, requests.HTTPError, requests.exceptions.SSLError) as e:
            print('Error occurred attempting to make an api request. {0}'.format(e))
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

    # -------------------------------------------------------------------------
    # SCOPE: FILES
    # -------------------------------------------------------------------------

    def get_file(self, key, version=None, geometry=None, plugin_data=None,
                 parent=None, return_raw_data=False):
        # https://www.figma.com/developers/api#get-files-endpoint
        """
        Get the JSON file contents for a file.
        """
        optional_data = ''
        if geometry or version or parent or plugin_data:
            optional_data = '?'
            if geometry:
                optional_data += f'geometry={geometry}'

            if optional_data != '?':
                optional_data += '&'
            if version:
                optional_data += f'version={version}'

            if optional_data != '?':
                optional_data += '&'
            if plugin_data:
                optional_data += f'plugin_data={plugin_data}'

        request = 'files/{0}{1}'.format(key, optional_data)

        data = self.api_request(request, method='get')
        if return_raw_data:
            return data


        if data is not None:

            # insert python helper attributes
            data['file_key'] = key
            data['pythonParent'] = parent

            return File(**data)

    def get_file_nodes(self, file_key, ids, version=None, depth=None, geometry=None, plugin_data=None):
        # https://www.figma.com/developers/api#get-file-nodes-endpoint
        """
        file_key: String, File to export JSON from
        ids: List of strings, A comma separated list of node IDs to retrieve and convert
        version: String, A specific version ID to get. Omitting this will get the current version of the file
        depth: Number, Positive integer representing how deep into the document tree to traverse. For example, setting this to 1 returns only Pages, setting it to 2 returns Pages and all top level objects on each page. Not setting this parameter returns all nodes
        geometry: String, Set to "paths" to export vector data
        plugin_data: String, A comma separated list of plugin IDs and/or the string "shared". Any data present in the document written by those plugins will be included in the result in the `pluginData` and `sharedPluginData` properties.
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

        data = self.api_request(f'files/{file_key}/nodes?ids={id_list}{optional_data}', method='get')
        return data
        # get partial JSON, only relevant data for the node. includes parent data.
        # nodes data can be accessed with data['nodes']

    def get_file_images(self, file_key, ids, scale=None, format=None, version=None):
        # https://www.figma.com/developers/api#get-images-endpoint
        """
        Get urls for server-side rendered images from a file.
        If the node is not an image, a rasterized version of the node will be returned.
        """
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
        data = self.api_request('images/{0}?ids={1}{2}'.format(file_key, id_list, optional_data), method='get')
        if data is not None:
            return FileImages(data['images'], data['err'])

    def get_image_fills(self, file_key):
        # https://www.figma.com/developers/api#get-image-fills-endpoint
        """
        Get urls for source images from a file. a fill is a user provided image
        """
        data = self.api_request(f'files/{file_key}/images', method='get')
        if data is not None:
            return data

    # -------------------------------------------------------------------------
    # SCOPE: FILES -> VERSIONS
    # -------------------------------------------------------------------------

    def get_file_versions(self, file_key):
        # https://www.figma.com/developers/api#get-file-versions-endpoint
        """
        Get the version history of a file.
        """
        data = self.api_request('files/{0}/versions'.format(file_key), method='get')
        if data is not None:
            # TODO check if data['pagination'] is still relevant, doesnt appear in docs
            return FileVersions(data['versions'], data['pagination'])

    # -------------------------------------------------------------------------
    # SCOPE: FILES -> COMMENTS
    # -------------------------------------------------------------------------

    def get_comments(self, file_key):
        # https://www.figma.com/developers/api#get-comments-endpoint
        """
        Get all comments on a file.
        """
        data = self.api_request('files/{0}/comments'.format(file_key), method='get')
        if data is not None:
            return Comments(data['comments'])

    def post_comment(self, file_key, message, client_meta=None):
        # https://www.figma.com/developers/api#post-comments-endpoint
        """
        Create a comment on a file.
        """
        print(client_meta)
        if client_meta is not None:
            payload = '{{"message":"{0}","client_meta":{1}}}'.format(message.title(), client_meta)
        else:
            payload = "{{'message':'{0}'}}".format(message)
        data = self.api_request('files/{0}/comments'.format(file_key), method='post', payload=payload)
        if data is not None:
            return Comment(data['id'], data['file_key'], data['parent_id'], data['user'], data['created_at'],
                           data['resolved_at'], data['message'], data['client_meta'], data['order_id'])

    def delete_comment(self):
        # https://www.figma.com/developers/api#delete-comments-endpoint
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # SCOPE: TEAMS -> PROJECTS
    # -------------------------------------------------------------------------
    def get_team_projects(self, team_id):
        """
        Get all projects for a team
        """
        # https://www.figma.com/developers/api#get-team-projects-endpoint
        data = self.api_request('teams/{0}/projects'.format(team_id), method='get')
        if data is not None:
            return TeamProjects(data['projects'])

    # -------------------------------------------------------------------------
    # SCOPE: PROJECTS -> FILES
    # -------------------------------------------------------------------------

    def get_project_files(self, project_id):
        """
        List the files in a given project (but don't load their content)
        """
        # https://www.figma.com/developers/api#get-project-files-endpoint
        project_data = self.api_request('projects/{0}/files'.format(project_id))
        # return ProjectFiles(project_data['files'])
        project = Project(name=project_data['name'], files=project_data['files'])
        return project.files

    # -------------------------------------------------------------------------
    # SCOPE: UTIL FUNCTIONS - NOT PART OF THE API
    # -------------------------------------------------------------------------

    def get_vector_images(self, file_key, nodes, scale=1, format='svg'):  # -> dict
        """
        get all non rasterized images as SVG-URLs
        figmaPy: FigmaPy.FigmaPy - the current figmaPy session
        nodes: list of FigmaPy.models.Node - the nodes to get the images from, do not use together with the ids kwarg
        scale: int - the scale to render the images at
        format: str - the format to return the images in

        this is the opposite of get_image_fills()

        returns: dict{node_id: image_url, ...}
        """
        vector_ids = []

        for node in nodes:
            for paint in node.fills:
                # anything that's not an image is assumed to be a vector
                if paint.type != 'IMAGE':
                    vector_ids.append(node.id)

        data = self.get_file_images(file_key, ids=vector_ids, scale=scale, format=format)
        return data.images