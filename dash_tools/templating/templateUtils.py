'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 19:12:04
 '''
from enum import Enum
from pkg_resources import resource_filename
import os


def _check_create_app_args(base_dir, app_name):
    """
    Check the arguments passed to the init command.
    """
    app_dir = os.path.join(base_dir, app_name)
    if os.path.exists(app_dir):
        exit(f'dash-tools: init: App {app_dir} already exists. Aborting.')


def _get_templates_data_path(data_dir: os.PathLike) -> os.PathLike:
    """
    Get the path to the data directory.
    """
    return resource_filename(__name__, data_dir)


class Templates(Enum):
    """
    Enum of templates to be used in the app.
    Values must match the file name in the templates directory.
    """
    DEFAULT = 'default'  # Default template multipage app.
    MINIMAL = 'minimal'  # Minial template for a simple app.
    HEROKU = 'heroku'  # Includes Heroku files.


def _convert_to_template_or_error(value) -> Templates:
    """
    Convert the string passed to the init command to a template.
    """
    try:
        return Templates(value)
    except ValueError:
        exit(
            f'dash-tools: init: Template "{value}" is not valid. Aborting.')
