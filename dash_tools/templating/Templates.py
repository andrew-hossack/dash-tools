'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:41:57
 # Templates file
'''
from enum import Enum


class Template(Enum):
    """
    Enum of templates to be used in the app.
    Values must match the file name in the templating/templates/ directory.
    """
    DEFAULT = 'default'                 # Default template multipage app
    TABS = 'tabs'                       # Tabs template from faculty.ai
    SIDEBAR = 'sidebar'                 # Sidebar template from faculty.ai
    IRIS = 'iris'                       # Iris K-Means Cluster - Interactively cluster the Iris dataset
    MULTIPAGE = 'multipage'         # Multipage app template using the multipage plugin.
