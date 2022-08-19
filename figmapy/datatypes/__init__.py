from .models import *
from .properties import *
from .nodes import *
from .results import *

"""
    to avoid circular imports, import in this order:

    FIGMAPY <──── DATATYPES
                    ↑
                    ├─── results
                    │      ↑
                    ├─── models
                    │      ↑
                    ├─── nodes ────────────┐
                    │      ↑               ↑
                    └─── properties <─── utils
"""

"""
    overview of datatypes:

    organisation?
    └─ TEAM
        └─ USER(s)

    TeamProjects (python helper wrapper)
    └─ PROJECT (collection of files which belong to user or team)
        └─ FILE_META (meta data about file)
            └─ FILES
                └─ VERSIONS
                └─ COMMENTS
                └─ DOCUMENT
                    └─  CANVAS / PAGES
                        └─  NODES
                            └─ NODES (optional children)
                                └─  ...
                └─ Components - variants, linked to a component set
                └─ ComponentSets - collection of variants

    COMPONENTS (metadata / styles in a team library)

    requested data is returned as dicts / JSON-s
    the figmaPy module converts these dicts into python objects,
    and adds meta data such as parent of node for user-friendly access
"""
