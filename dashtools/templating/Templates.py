'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:41:57
 # @ Templates file
'''
from enum import Enum


class Template(Enum):
    """
    Enum of templates to be used in the app.
    Values must match the directory name in the templating/templates/ directory

    e.g.
    -> DEFAULT = 'default'
    -> Here the template 'DEFAULT' has a template directory named '/default':
    -> templates/default/
    """
    ADVANCED = 'advanced'
    CSV = 'csv'
    DEFAULT = 'default'
    FASTDASH = 'fastdash'
    ICONIFY = 'iconify'
    IRIS = 'iris'
    MANTINE = 'mantine'
    MULTIPAGE = 'multipage'
    SIDEBAR = 'sidebar'
    TABS = 'tabs'
