# result wrappers for GET commands
from FigmaPy.datatypes.models import Comment


class FileImages:
    # URLs for server-side rendered images from a file
    # https://www.figma.com/developers/api#get-images-endpoint
    def __init__(self, images, err):
        self.err = err  # Error type as enum string
        self.images = images  # -> dict{nodeId: url, ...} URLs of server-side rendered images from a file


class FileVersions:
    # Version history from a file
    def __init__(self, versions, pagination):
        self.versions = versions  # Version from a file
        self.pagination = pagination  # Pagination from a file


class Comments:
    # todo replace with array of classes type comment
    # Comment(s) from a file
    def __init__(self, comments):
        self.comments = None  # Comment(s) from a file

        if len(comments) > 0 or comments is not None:
            self.comments = []
            for comment in comments:
                self.comments.append(Comment(comment['id'], comment['file_key'], comment['parent_id'], comment['user'],
                                             comment['created_at'], comment['resolved_at'], comment['message'],
                                             comment['client_meta'], comment['order_id']))


class TeamProjects:
    # todo replace with array of classes type project
    # Projects from a team
    def __init__(self, projects):
        self.projects = projects  # Projects from a team

    def get_project_name_by_id(self, id):
        for project in self.projects:
            if project['id'] == id:
                return project['name']

    def get_project_id_by_name(self, name):
        for project in self.projects:
            if project['name'] == name:
                return project['id']


class ProjectFiles:
    # todo replace with array of classes type file
    # Files from a project
    def __init__(self, files):
        self.files = files  # Files from a project
