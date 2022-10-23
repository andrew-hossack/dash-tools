'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-05-23 12:48:14
 # Generate interesting app names
'''

import random
from pkg_resources import resource_filename
import os


def _get_data_path(filename: os.PathLike) -> os.PathLike:
    """
    Get the path to the data directory.
    """
    return resource_filename(__name__, filename)


def get_words(N: int) -> list:
    """
    Get N random words from the data file.
    """
    with open(_get_data_path('nounlist.csv'), 'r') as f:
        words = f.read().splitlines()
    return [words[i] for i in sorted(random.sample(range(len(words)), N))]
