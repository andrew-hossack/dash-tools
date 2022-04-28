'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:23:14
'''
import os
import re
import subprocess
import webbrowser
from typing import Union

from dash_tools.deploy import fileUtils, gitUtils, herokuUtils


def _check_required_files_exist(root_path: os.PathLike) -> bool:
    """
    Check for Procfile, runtime.txt, requirements.txt
    """
    deploy_should_continue = True
    # Check if procfile exists
    if not fileUtils.check_file_exists(root_path, 'Procfile'):
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file Procfile not found. Create one automatically?'):
            fileUtils.create_procfile(root_path)
        else:
            deploy_should_continue = False
    # Check for the Runtime file
    if (not fileUtils.check_file_exists(root_path, 'runtime.txt')) and deploy_should_continue:
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file runtime.txt not found. Create one automatically?'):
            fileUtils.create_runtime_txt(root_path)
        else:
            deploy_should_continue = False
    # Check for the Requirements file
    if (not fileUtils.check_file_exists(root_path, 'requirements.txt')) and deploy_should_continue:
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file requirements.txt not found. Create one automatically?'):
            fileUtils.create_requirements_txt(root_path)
        else:
            deploy_should_continue = False
    return deploy_should_continue


def _prompt_user_choice(message: str, prompt: str = 'Continue? (y/n) > ', does_repeat: bool = True) -> bool:
    """
    Prompt the user to continue or not.

    Args:
        message: Message to display to the user
        prompt: Prompt to display to the user
        does_repeat: If True, the user will be prompted again if they enter an invalid response

    Returns:
        True (y/Y)
        False (n/N)
    """
    print(message)
    response = input(f'dash-tools: {prompt}')
    if response.lower() == 'y':
        return True
    elif response.lower() == 'n':
        return False
    elif does_repeat:
        return _prompt_user_choice(message)
    else:
        return False


def _add_changes_and_push_to_heroku(heroku_app_name: str) -> bool:
    """
    Add changes to the repository and push to Heroku

    Returns:
        True (Success)
        False (Failure)
    """
    # Create a commit to push to Heroku
    print(f'dash-tools: deploy-heroku: Creating commit to push to Heroku')
    os.system(f'git add .')
    os.system(
        f'git commit -m "Deploy to Heroku for app {heroku_app_name} - dash-tools"')
    # Push to Heroku
    print(f'dash-tools: deploy-heroku: Pushing to Heroku')
    try:
        subprocess.check_output(
            f'git push heroku HEAD:master', shell=True)
    except subprocess.CalledProcessError:
        return False
    return True


def _remove_heroku_remote():
    """
    Remove the heroku remote

    Returns:
        True if successful
        False if failed
    """
    print('dash-tools: deploy-heroku: Removing existing heroku remote')
    try:
        subprocess.check_output('git remote rm heroku', shell=True)
    except subprocess.CalledProcessError:
        exit('dash-tools: deploy-heroku: Failed to remove heroku remote')


def _check_heroku_remote_already_exists() -> bool:
    """
    Check if the heroku remote is set

    Returns:
        True if already set
        False if remote "heroku" is not set
    """
    regex = r'heroku'
    try:
        output = subprocess.check_output('git remote', shell=True)
        heroku_grep = re.search(regex, output.decode('utf-8'))
        try:
            heroku_grep.group(0)
        except AttributeError:
            return False
    except subprocess.CalledProcessError:
        exit('dash-tools: deploy-heroku: Failed to check if heroku remote is set')
    return True


def _success_message(heroku_app_name: str):
    """
    Print a success message
    """
    print(f'\n\ndash-tools: deploy-heroku: Successfully deployed to Heroku from git branch "heroku"!')
    print(
        f'dash-tools: deploy-heroku: To push changes, select the "Update Existing App" option after typing: dash-tools --deploy-heroku')
    print(
        f'dash-tools: deploy-heroku: Management Page: https://dashboard.heroku.com/apps/{heroku_app_name}')
    print(
        f'dash-tools: deploy-heroku: Application Page: https://{heroku_app_name}.herokuapp.com/')

    # Prompt user to open the deployed app
    if input('dash-tools: deploy-heroku: Enter any key to open in browser or q to exit > ') != 'q':
        webbrowser.open(f'https://{heroku_app_name}.herokuapp.com/')


def _get_valid_app_name(heroku_app_name: str) -> str:
    """
    Returns a unique and valid heroku app name
    """
    # Generate or let user type in app name if it is not provided
    if not heroku_app_name:
        heroku_app_name = herokuUtils.get_heroku_app_name()

    # Wait for user to input a correct name
    should_continue = False
    while not should_continue:
        # Check if the project already exists on Heroku if name is specified
        if not herokuUtils.check_heroku_app_name_available(heroku_app_name):
            print(
                f'dash-tools: deploy-heroku: App "{heroku_app_name}" already exists on Heroku!')
            print(
                'dash-tools: deploy-heroku: Please choose a unique name that isn\'t already taken.')
            heroku_app_name = herokuUtils.get_heroku_app_name()
        elif not herokuUtils.validate_heroku_app_name(heroku_app_name):
            print(
                f'dash-tools: deploy-heroku: App name "{heroku_app_name}" is not valid!')
            print('dash-tools: deploy-heroku: Heroku app names must start with a letter, end with a letter or digit, can only contain lowercase letters, numbers, and dashes, and have a minimum length of 3 characters.')
            heroku_app_name = herokuUtils.get_heroku_app_name()
        else:
            should_continue = True
    return heroku_app_name


def deploy_app_to_heroku(project_root_dir: os.PathLike, heroku_app_name: Union[str, None]):
    """
    Uses the Heroku CLI to deploy the current project
    """
    print('dash-tools: deploy-heroku: Starting')

    # Check if heroku CLI is installed
    if not herokuUtils.heroku_is_installed():
        print(f'dash-tools: deploy-heroku: Heroku CLI not installed!')
        print(f'dash-tools: deploy-heroku: See https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli')
        exit('dash-tools: deploy-heroku: Failed')

    # Check if git is installed
    if not gitUtils.git_is_installed():
        print(f'dash-tools: deploy-heroku: Git not installed!')
        print(f'dash-tools: deploy-heroku: See https://git-scm.com/downloads')
        exit('dash-tools: deploy-heroku: Failed')

    # Check that git is initialized in the current repo
    if not gitUtils.is_git_repository():
        print(f'dash-tools: deploy-heroku: Current directory is not a git repository!')
        print('dash-tools: deploy-heroku: To start a git repository, type: git init')
        exit('dash-tools: deploy-heroku: Failed')

    # Check that heroku remote is not already set
    if _check_heroku_remote_already_exists():
        print(f'dash-tools: deploy-heroku: Git remote "heroku" is already set!')
        print('dash-tools: deploy-heroku: Please choose an option below:')
        print('\t1. Push to the existing heroku remote (Update Existing App)')
        print('\t2. Remove the heroku remote and continue (Create New App)')
        print('\t3. Abort')
        should_continue = False
        while not should_continue:
            response = input('dash-tools: Choice (1, 2, 3) > ')
            if response == '1':
                if not _add_changes_and_push_to_heroku(heroku_app_name):
                    exit('dash-tools: deploy-heroku: Failed to push to heroku')
                print('dash-tools: deploy-heroku: Changes pushed to heroku remote')
                exit('dash-tools: deploy-heroku: Success')
            elif response == '2':
                _remove_heroku_remote()
                should_continue = True
            elif response == '3':
                exit('dash-tools: deploy-heroku: Aborted')
            else:
                should_continue = False

    # Get a unique app name
    heroku_app_name = _get_valid_app_name(heroku_app_name)

    # Check that the project has necessary files
    if not _check_required_files_exist(project_root_dir):
        print('dash-tools: deploy-heroku: Procfile, runtime.txt, and requirements.txt are needed for Heroku deployment.')
        exit('dash-tools: deploy-heroku: Aborted')

    # Check procfile is correct
    procfile = fileUtils.verify_procfile(project_root_dir)
    if not procfile['valid']:
        print(
            f'dash-tools: deploy-heroku: Procfile is incorrect. Did you include "{procfile["hook"]} = app.server" after instantiating "app = Dash(...)" in {procfile["dir"]}/{procfile["module"]}?')
        print(
            'dash-tools: deploy-heroku: See https://devcenter.heroku.com/articles/procfile')
        exit('dash-tools: deploy-heroku: Failed')

    # Log into Heroku
    if not herokuUtils.login_heroku_successful():
        print(f'dash-tools: deploy-heroku: Heroku login failed.')
        exit('dash-tools: deploy-heroku: Failed')

    # Confirm deployment settings and create the project on Heroku if the user confirms
    if not _prompt_user_choice(f'dash-tools: deploy-heroku: Please confirm creating app {heroku_app_name} on Heroku and adding git remote "heroku".'):
        exit('dash-tools: deploy-heroku: Aborted')

    # Create the project on Heroku and capture the git remote URL
    if not herokuUtils.create_app_on_heroku(heroku_app_name):
        exit(
            f'dash-tools: deploy-heroku: Deploying app {heroku_app_name} to Heroku failed.')

    # Add python buildpack
    print(f'dash-tools: deploy-heroku: Adding python buildpack')
    os.system(f'heroku buildpacks:add heroku/python -a {heroku_app_name}')

    # Push to Heroku
    _add_changes_and_push_to_heroku(heroku_app_name)

    # Print success message and exit
    _success_message(heroku_app_name)
