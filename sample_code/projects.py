import FigmaPy

team_key = 'REDACTED'
auth_key = 'REDACTED'

figmaPy = FigmaPy.FigmaPy(auth_key)

projects = figmaPy.get_team_projects(team_key)
# projects:  [{'id': '34443824', 'name': 'Visual Style Guide'}]

# get the files from a project
project_id = projects.projects[0]['id']
files = figmaPy.get_project_files(project_id)
for fileMeta in files:
    print(fileMeta.get_file_content(figmaPy))
    # <FigmaPy.datatypes.models.File object at 0x000001BB9A1B9FD0>
