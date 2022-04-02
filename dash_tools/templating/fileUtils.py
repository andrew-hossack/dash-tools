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
