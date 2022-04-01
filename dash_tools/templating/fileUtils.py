'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 16:24:15
'''
from typing import IO
from pkg_resources import resource_filename
import datetime
import os


def _get_data_path(data_dir: os.PathLike) -> os.PathLike:
    return resource_filename(__name__, data_dir)


def format_file_stream(t: IO, app_name: str) -> str:
    """
    Format the template file with given variables.
    """
    w = t.read().replace(r'{appName}', app_name)
    w = w.replace(r'{createTime}', str(datetime.datetime.now()))
    # w = w.replace(r'{foo}', 'bar')
    return w


def _make_base_src_dir(base_dir: os.PathLike, app_name: str):
    """
    Creates a new directory for the app's src files.
    Returns: (BASE_DIR, APP_SRC_DIR)
    """
    base_dir = os.path.join(base_dir, app_name)

    if os.path.exists(base_dir):
        exit(f'dash-tools: init: App {base_dir} already exists! Aborting.')

    # ./AppName/
    os.makedirs(base_dir)
    # ./AppName/AppName
    app_src_dir = os.path.join(base_dir, app_name)
    os.makedirs(app_src_dir)
    return base_dir, app_src_dir
