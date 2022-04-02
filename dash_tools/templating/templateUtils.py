'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 19:12:04
 '''

from enum import Enum
from pkg_resources import resource_filename
import os


def _get_data_path(data_dir: os.PathLike) -> os.PathLike:
    return resource_filename(__name__, data_dir)


class Templates(Enum):
    """
    Enum of templates to be used in the app.
    Values must match the file name in the templates directory.
    """
    DEFAULT = 'default'
    MINIMAL = 'minimal'
