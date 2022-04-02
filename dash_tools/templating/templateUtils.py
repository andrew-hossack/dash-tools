'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 19:12:04
 '''
from enum import Enum
from pkg_resources import resource_filename
import os


def _check_args(base_dir, app_name):
    # Check if the app already exists
    app_dir = os.path.join(base_dir, app_name)
    if os.path.exists(app_dir):
        exit(f'dash-tools: init: App {app_dir} already exists. Aborting.')


def _get_data_path(data_dir: os.PathLike) -> os.PathLike:
    return resource_filename(__name__, data_dir)


class Templates(Enum):
    """
    Enum of templates to be used in the app.
    Values must match the file name in the templates directory.
    """
    DEFAULT = 'default'
    MINIMAL = 'minimal'


def _convert_to_template_or_error(value) -> Templates:
    try:
        return Templates(value)
    except ValueError:
        exit(
            f'dash-tools: init: Template "{value}" is not valid. Aborting.')
