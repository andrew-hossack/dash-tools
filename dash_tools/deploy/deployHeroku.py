'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:23:14
'''
import os
import re
import subprocess


def _heroku_is_installed() -> bool:
    """
    Check that heroku CLI is installed on the system
    Looks for "heroku/X.Y.Z ..." in the output of "heroku --version"
    """
    regex = r'[a-zA-Z]+/[0-9]+\.[0-9]+\.[0-9]+'
    isInstalled = True
    try:
        heroku_command_output = subprocess.check_output(
            'heroku --version', shell=True)
        if not re.search(regex, heroku_command_output.decode('utf-8')):
            isInstalled = False
    except subprocess.CalledProcessError:
        isInstalled = False
    return isInstalled


def _check_file_exists(root_path: os.PathLike, file_name: str):
    """
    Check that a file exists
    """
    path = os.path.join(root_path, file_name)
    if not os.path.exists(path):
        print(
            f'dash-tools: deploy-heroku: {file_name} not found in {root_path} - is the project configured for Heroku?')
        exit(1)


def deploy_app_to_heroku(project_root_dir: os.PathLike):
    """
    Uses the Heroku CLI to deploy the current project
    """
    # Check if heroku CLI is installed
    if not _heroku_is_installed():
        print(f'dash-tools: deploy-heroku: Heroku CLI not installed!')
        print(f'dash-tools: See https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli')
        exit(1)

    print(f'dash-tools: deploy-heroku: Deploying to Heroku...')

    # Check that Procfile exists
    _check_file_exists(project_root_dir, 'Procfile')

    # Check that runtime.txt exists
    _check_file_exists(project_root_dir, 'runtime.txt')

    # Check that requirements.txt exists
    _check_file_exists(project_root_dir, 'requirements.txt')
