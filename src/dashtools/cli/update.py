'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-08-09 10:17:39
 # Checks for newer versions of dash-tools with yolk3k and prompt updates if available
'''


import re
import subprocess
from typing import Union

from dashtools.version import __version__
from termcolor import cprint


def _new_version_available() -> Union[str, None]:
    """
    Checks for newer version using yolk3k

    Returns:
        str: New version if available, None if not
    """
    regex = r'\([0-9]+\.[0-9]+\.[0-9]+\)'
    try:
        response = subprocess.check_output(
            'yolk -U dash-tools',
            shell=True,
            stderr=subprocess.DEVNULL)
        version = re.search(regex, response.decode('utf-8'))
        return version.group(0) if version.group(0).strip('(').strip(')') != __version__ else None
    except subprocess.CalledProcessError:
        # Problem with checking for updates; fail gracefully
        cprint(
            f"WARNING: There was an error checking the latest version of dash-tools.", 'yellow')
        return None


def check_for_updates():
    """
    Check for new version of dash-tools and prompt update if available
    """
    new_version = _new_version_available()
    if new_version:
        cprint(
            f"INFO: You are using dash-tools version {__version__}, however version {new_version.strip('(').strip(')')} is available.\nINFO: You should consider upgrading via the 'python -m pip install --upgrade dash-tools' command.", 'yellow')
