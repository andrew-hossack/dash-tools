'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:23:14
'''
import os
import re
import subprocess
import uuid


def _heroku_is_installed() -> bool:
    """
    Check that heroku CLI is installed on the system
    Looks for "heroku/X.Y.Z ..." in the output of "heroku --version"
    """
    regex = r'heroku/[0-9]+\.[0-9]+\.[0-9]+ [a-zA-Z]+'
    isInstalled = True
    try:
        heroku_command_output = subprocess.check_output(
            'heroku --version', shell=True)
        if not re.search(regex, heroku_command_output.decode('utf-8')):
            isInstalled = False
    except subprocess.CalledProcessError:
        isInstalled = False
    return isInstalled


def _git_is_installed() -> bool:
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


def _check_file_exists(root_path: os.PathLike, file_name: str):
    """
    Check that a file exists
    """
    path = os.path.join(root_path, file_name)
    if not os.path.exists(path):
        print(
            f'dash-tools: deploy-heroku: {file_name} not found in {root_path} - is the project configured for Heroku?')
        exit(1)


def _is_git_initialized() -> bool:
    """
    Check that the current location is a git repository or not
    """
    regex = r'fatal: not a git repository'
    isGitInitialized = True
    try:
        git_command_output = subprocess.check_output(
            'git remote -v', shell=True)
        if re.search(regex, git_command_output.decode('utf-8')):
            isGitInitialized = False
    except subprocess.CalledProcessError:
        isGitInitialized = False
    return isGitInitialized


def _login_heroku_successful() -> bool:
    """
    Try to log into Heroku
    """
    print(f'dash-tools: deploy-heroku: Logging into Heroku...')
    regex = r'Error: quit'
    loginWasSuccessful = True
    try:
        heroku_command_output = subprocess.check_output(
            'heroku login', shell=True)
        if re.search(regex, heroku_command_output.decode('utf-8')):
            loginWasSuccessful = False
    except subprocess.CalledProcessError:
        loginWasSuccessful = False
    return loginWasSuccessful


def _create_app_on_heroku(app_name: str) -> str or None:
    """
    Create the project on Heroku and return the git remote URL
    """
    print(f'dash-tools: deploy-heroku: Creating {app_name} on Heroku...')
    heroku_command_output = subprocess.check_output(
        f'heroku create {app_name}', shell=True)
    regex = 'https:\/\/git\.heroku\.com\/[a-zA-Z0-9-_]*\.git'
    git_remote_url = re.search(
        regex, heroku_command_output.decode('utf-8'))
    try:
        git_remote_url = git_remote_url.group(0)
    except AttributeError:
        git_remote_url = None
    return git_remote_url


def deploy_app_to_heroku(project_root_dir: os.PathLike, app_name: str):
    """
    Uses the Heroku CLI to deploy the current project
    """
    # Check if heroku CLI is installed
    if not _heroku_is_installed():
        print(f'dash-tools: deploy-heroku: Heroku CLI not installed!')
        print(f'dash-tools: See https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli')
        exit('dash-tools: deploy-heroku: Failed')

    # # Check if git is installed TODO: Check if git is installed
    if not _git_is_installed():
        print(f'dash-tools: deploy-heroku: Git not installed!')
        print(f'dash-tools: See https://git-scm.com/downloads')
        exit('dash-tools: deploy-heroku: Failed')

    # Check that Procfile exists
    _check_file_exists(project_root_dir, 'Procfile')

    # Check that runtime.txt exists
    _check_file_exists(project_root_dir, 'runtime.txt')

    # Check that requirements.txt exists
    _check_file_exists(project_root_dir, 'requirements.txt')

    # Log into Heroku
    if not _login_heroku_successful():
        print(f'dash-tools: deploy-heroku: Failed to log into Heroku!')
        exit('dash-tools: deploy-heroku: Failed')

    # Check that the project is not already on Heroku
    print(
        f'dash-tools: deploy-heroku: Checking if {app_name} is already on Heroku...')
    heroku_command_output = subprocess.check_output(
        f'heroku apps', shell=True)
    if app_name in heroku_command_output.decode('utf-8'):
        print(
            f'dash-tools: deploy-heroku: {app_name} is already on Heroku. Please choose a unique name.')
        exit('dash-tools: deploy-heroku: Failed')

    # Create the project on Heroku and capture the git remote URL
    git_remote_url = _create_app_on_heroku(app_name)
    if not git_remote_url:
        print(
            f'dash-tools: deploy-heroku: Failed to create {app_name} on Heroku!')
        exit('dash-tools: deploy-heroku: Failed')

    # Add python buildpack
    print(f'dash-tools: deploy-heroku: Adding python buildpack...')
    os.system(f'heroku buildpacks:add heroku/python -a {app_name}')

    # Check that git is initialized in the current repo
    if not _is_git_initialized():
        print(f'dash-tools: deploy-heroku: Initializing git...')
        # Initialize git
        os.system(f'git init')
        # Create branch
        os.system(f'git checkout -b main')

    # Create a commit to push to Heroku
    print(f'dash-tools: deploy-heroku: Creating commit to push to Heroku...')
    os.system(f'git add .')
    os.system(f'git commit -m "Initial deploy to Heroku for {app_name}"')

    # Create remote Heroku repository with the git remote URL and 4 digit uuid
    heroku_remote_name = f'heroku-{uuid.uuid4().hex[:4]}'

    # Add git heroku remote
    print(
        f'dash-tools: deploy-heroku: Adding git remote "{heroku_remote_name}" to git...')
    os.system(f'git remote add {heroku_remote_name} {git_remote_url}')

    # Push to Heroku
    print(f'dash-tools: deploy-heroku: Pushing to Heroku...')
    os.system(f'git push {heroku_remote_name} main')

    print(
        f'dash-tools: deploy-heroku: Published to Heroku remote: {heroku_remote_name} on branch main')
    print(f'dash-tools: deploy-heroku: Successfully deployed to Heroku!')
    print(
        f'dash-tools: deploy-heroku: Management Page https://dash.herokuapp.com/apps/{app_name}')
    print(
        f'dash-tools: deploy-heroku: Deployed To https://{app_name}.herokuapp.com/')
