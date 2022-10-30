'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 11:43:00
 # Git util functions
'''
import os
import re
import subprocess
from typing import Union


def git_is_installed() -> bool:
    """
    Check that git is installed on the system
    """
    regex = r'git version'
    isInstalled = True
    try:
        git_command_output = subprocess.check_output(
            'git --version', shell=True)
        if not re.search(regex, git_command_output.decode('utf-8')):
            isInstalled = False
    except subprocess.CalledProcessError:
        isInstalled = False
    return isInstalled


def is_git_repository(cwd: os.PathLike = None) -> bool:
    """
    Check that the current location is a git repository or not
    by checking .git directory
    """
    path = '.git'
    if cwd:
        path = os.path.join(cwd, '.git')
    if os.path.isdir(path):
        return True
    return False


def get_remote_url(cwd: os.PathLike) -> Union[str, None]:
    """
    returns git config --get remote.origin.url (str or None if not found)
    recommended to check git is installed before calling this
    """
    return os.popen(f'cd {cwd} && git config --get remote.origin.url').read().replace('\n', '')


def commit_and_push(cwd: os.PathLike, commit_message: str = ''):
    commit_message = commit_message.replace('"', '').replace("'", '')
    os.popen(
        f'cd {cwd} && git add . && git commit -m "{commit_message}" && git push --set-upstream origin master')
