'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 11:43:00
 # Git util functions
'''
import os
import re
import subprocess


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


def is_git_repository() -> bool:
    """
    Check that the current location is a git repository or not
    by checking .git directory
    """
    isGitRepo = False
    if os.path.isdir('.git'):
        isGitRepo = True
    return isGitRepo
