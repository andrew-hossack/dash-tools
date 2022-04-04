'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:41:57
 # Templates file
'''
from enum import Enum


class Template(Enum):
    """
    Enum of templates to be used in the app.
    Values must match the file name in the templates directory.
    """
    DEFAULT = 'default'  # Default template multipage app.
    MINIMAL = 'minimal'  # Minial template for a simple app.
    HEROKU = 'heroku'    # Includes Heroku files.
