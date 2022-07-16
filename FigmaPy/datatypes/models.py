# API Scope Resource Objects

# todo make class subscribe-able. so we can do both node.items or node['items']
# todo add property get set to attributes. so we can auto cast to correct type. accept both dict or type
from typing import List

from . import nodes


# -------------------------------------------------------------------------
# GENERAL API TYPES
# -------------------------------------------------------------------------
class Project:
    def __init__(self, name, files, _parent=None):
        self.name = name  # -> string - Project name
        self.files = self.deserialize_files(files, _parent=self)

        # python helpers
        self._parent = _parent

    @staticmethod
    def deserialize_files(files, _parent=None):
        deserialized_files: List[FileMeta] = []
        for data in files:
            fileMeta = FileMeta(key=data['key'],
                                last_modified=data['last_modified'],
                                name=data['name'],
                                thumbnail_url=data['thumbnail_url'],
                                branches=data.get('branches', None),
                                _parent=_parent)
            deserialized_files.append(fileMeta)
        return deserialized_files


class FileMeta:
    """
    this lives inside a project. used to get file content => class File
    """
    def __init__(self, key, last_modified, name, thumbnail_url, branches=None, _parent=None):
        self.key: str = key
        self.last_modified: str = last_modified
        self.name: str = name
        self.thumbnail_url: str = thumbnail_url
        self.branches = branches  # -> array of Branch metadata # todo deserialize branches

        # python helpers
        self._parent = _parent  # the project this file belongs to
        self._file_key: str = self.key

    def get_file_content(self, figmaPy, geometry=None, version=None):
        """
        load the file from the server
        """
        return figmaPy.get_file(key=self.key, geometry=geometry, version=version, parent=self)


class File:
    """
    # JSON file contents from a file
    """
    def __init__(self, name, document, components, componentSets, lastModified, thumbnailUrl, styles, schemaVersion=0,
                version=None, role=None, editorType=None, linkAccess=None, mainFileKey=None, branches=None,
                 _parent=None):
        self.name = name  # File name
        self.role = role
        self.lastModified = lastModified  # Date file was last modified
        self.editorType = editorType
        self.thumbnailUrl = thumbnailUrl  # File thumbnail URL
        self.version = version
        self.document = nodes.Document(**document, _parent=self)  # Document content from a file
        self.components = components  # Document components from a file
        self.componentSets = componentSets
        self.schemaVersion = schemaVersion  # Schema version from a file
        self.styles = styles  # Styles contained within a file
        self.mainFileKey = mainFileKey
        self.branches = branches
        self.linkAccess = linkAccess  # TODO check if this only appears in branch files

        # python helpers
        self._parent = _parent  # using underscore to mark var as python helper, instead of a figma api var


class Comment:
    # A comment or reply left by a user
    def __init__(self, id, file_key, parent_id, user, created_at, resolved_at, message, client_meta, order_id):
        self.id = id  # Unique identifier for comment
        self.file_key = file_key  # The file in which the comment lives
        self.parent_id = parent_id  # If present, the id of the comment to which this is the reply
        self.user = user  # The user who left the comment
        self.created_at = created_at  # The UTC ISO 8601 time at which the comment was left
        self.resolved_at = resolved_at  # If set, the UTC ISO 8601 time the comment was resolved
        self.message = message  # Content of comment
        self.client_meta = client_meta  # The position of the comment. Absolute coordinates or relative offset
        self.order_id = order_id  # Only set for top level comments. The number displayed with the comment in the UI


class User:  # todo not yet used, hookup
    # A description of a user
    def __init__(self, handle, img_url):
        self.handle = handle  # Name of the user
        self.img_url = img_url  # URL link to the user's profile image


class Version:  # todo not yet used, hookup
    # A version of a file
    def __init__(self, id, created_at, label, description, user):
        self.id = id  # Unique identifier for version
        self.created_at = created_at  # the UTC ISO 8601 time at which the version was created
        self.label = label  # The label given to the version in the editor
        self.description = description  # The description of the version as entered in the editor
        self.user = user  # The user that created the version
