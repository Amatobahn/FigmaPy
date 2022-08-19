import figmapy.datatypes.models as models
import figmapy

files = [
    {
        'key': 'file_key',
        'last_modified': 'last_modified',
        'name': 'name',
        'thumbnail_url': 'thumbnail_url',
        'branches': [],
    },
]


class TestProject:
    def test_create_project(self):
        name = 'Test Project Name'
        project = models.Project(name=name, files=files)
        assert project.name == name


def test_get_file():
    session = figmapy.FigmaPy(token='api_key')

    def api_request(*args, **kwargs):
        """this is the result of running get_file on an empty figma file on 8 aug 2022
        thumb url was shortened"""
        return {
            'document': {
                'id': '0:0',
                'name': 'Document',
                'type': 'DOCUMENT',
                'children': [
                    {
                        'id': '0:1',
                        'name': 'Page 1',
                        'type': 'CANVAS',
                        'children': [],
                        'backgroundColor': {
                            'r': 0.11764705926179886,
                            'g': 0.11764705926179886,
                            'b': 0.11764705926179886,
                            'a': 1.0,
                        },
                        'prototypeStartNodeID': None,
                        'flowStartingPoints': [],
                        'prototypeDevice': {'type': 'NONE', 'rotation': 'NONE'},
                    }
                ],
            },
            'components': {},
            'componentSets': {},
            'schemaVersion': 0,
            'styles': {},
            'name': 'Untitled',
            'lastModified': '2022-08-19T23:01:51Z',
            'thumbnailUrl': 'https://test',
            'version': '2239202519',
            'role': 'owner',
            'editorType': 'figma',
            'linkAccess': 'org_view',
        }

    session.api_request = api_request
    file = session.get_file(key='file_key', geometry='geometry', version='version')

    # check document and pages
    assert file.document.pages[0]
