"""Result wrappers for GET commands"""

from FigmaPy.datatypes.models import Comment


class FileImages:
    """
    URLs for server-side rendered images from a file

    Figma Docs: https://www.figma.com/developers/api#get-images-endpoint
    """

    def __init__(self, images, err):
        """Create a new instance of FileImages"""
        self.err = err  # Error type as enum string
        self.images = images  # -> dict{nodeId: url, ...} URLs of server-side rendered images from a file


class FileVersions:
    """Version history from a file"""

    def __init__(self, versions, pagination):
        """Create a new instance of FileVersions"""
        self.versions = versions  # Version from a file
        self.pagination = pagination  # Pagination from a file


class Comments:
    """
    Comment(s) from a file

    TODO: replace with array of classes type comment
    """

    def __init__(self, comments):
        """Create a new instance of Comments"""
        self.comments = None  # Comment(s) from a file

        if len(comments) > 0 or comments is not None:
            self.comments = []
            for comment in comments:
                self.comments.append(
                    Comment(
                        comment["id"],
                        comment["file_key"],
                        comment["parent_id"],
                        comment["user"],
                        comment["created_at"],
                        comment["resolved_at"],
                        comment["message"],
                        comment["client_meta"],
                        comment["order_id"],
                    )
                )


class TeamProjects:
    """
    Projects from a team

    TODO: replace with array of classes type project
    """

    def __init__(self, projects):
        """Create a new instance of TeamProjects"""
        self.projects = projects  # Projects from a team

    def get_project_name_by_id(self, id):
        """Retrieve Project Name by ID"""
        for project in self.projects:
            if project["id"] == id:
                return project["name"]

    def get_project_id_by_name(self, name):
        """Retrieve Project ID by Name"""
        for project in self.projects:
            if project["name"] == name:
                return project["id"]


# class ProjectFiles:
#     # todo replace with array of classes type file
#     # Files from a project
#     def __init__(self, files):
#         self.files = files  # Files from a project
