# API Scope Resource Objects


class File:
    def __init__(self, name, document, components, last_modified, thumbnail_url, schema_version, styles):
        self.name = name
        self.last_modified = last_modified
        self.thumbnail_url = thumbnail_url
        self.document = document
        self.components = components
        self.schema_version = schema_version
        self.styles = styles


class FileImages:
    def __init__(self, images, err):
        self.err = err
        self.images = images


class FileVersions:
    def __init__(self, versions, pagination):
        self.versions = versions
        self.pagination = pagination


class Comments:
    def __init__(self, comments):
        self.comments = None

        if len(comments) > 0 or comments is not None:
            self.comments = []
            for comment in comments:
                self.comments.append(Comment(comment['id'], comment['file_key'], comment['parent_id'], comment['user'],
                                             comment['created_at'], comment['resolved_at'], comment['message'],
                                             comment['client_meta'], comment['order_id']))


class Comment:
    def __init__(self, id, file_key, parent_id, user, created_at, resolved_at, message, client_meta, order_id):
        self.id = id
        self.file_key = file_key
        self.parent_id = parent_id
        self.user = user
        self.created_at = created_at
        self.resolved_at = resolved_at
        self.message = message
        self.client_meta = client_meta
        self.order_id = order_id


class TeamProjects:
    def __init__(self, projects):
        self.projects = projects

    def get_project_name_by_id(self, id):
        for project in self.projects:
            if project['id'] == id:
                return project['name']

    def get_project_id_by_name(self, name):
        for project in self.projects:
            if project['name'] == name:
                return project['id']


class ProjectFiles:
    def __init__(self, files):
        self.files = files
