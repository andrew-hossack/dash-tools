'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:23:14
'''
import os
import re
import subprocess
import webbrowser

from dash_tools.deploy import fileUtils, gitUtils, herokuUtils


def _check_required_files_exist(root_path: os.PathLike) -> bool:
    """
    Check for Procfile, runtime.txt, requirements.txt
    """
    deploy_should_continue = True
    # Check if procfile exists
    if not fileUtils.check_file_exists(root_path, 'Procfile'):
        if prompt_user_choice(
                'dash-tools: Required file Procfile not found. Create one automatically?'):
            fileUtils.create_procfile(root_path)
        else:
            deploy_should_continue = False
    # Check for the Runtime file
    if (not fileUtils.check_file_exists(root_path, 'runtime.txt')) and deploy_should_continue:
        if prompt_user_choice(
                'dash-tools: Required file runtime.txt not found. Create one automatically?'):
            fileUtils.create_runtime_txt(root_path)
        else:
            deploy_should_continue = False
    # Check for the Requirements file
    if (not fileUtils.check_file_exists(root_path, 'requirements.txt')) and deploy_should_continue:
        if prompt_user_choice(
                'dash-tools: Required file requirements.txt not found. Create one automatically?'):
            fileUtils.create_requirements_txt(root_path)
        else:
            deploy_should_continue = False
    return deploy_should_continue


def prompt_user_choice(message: str, prompt: str = 'Continue? (y/n) > ', does_repeat: bool = True) -> bool:
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
        return prompt_user_choice(message)
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
    print(f'dash-tools: Creating commit to push to Heroku')
    os.system(f'git add .')
    os.system(
        f'git commit -m "Deploy to Heroku for app {heroku_app_name} - dash-tools"')
    # Push to Heroku
    print(f'dash-tools: Pushing to Heroku')
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
    print('dash-tools: Removing existing heroku remote')
    try:
        subprocess.check_output('git remote rm heroku', shell=True)
    except subprocess.CalledProcessError:
        exit('dash-tools: heroku: deploy: Failed to remove heroku remote')


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
        exit('dash-tools: heroku: deploy: Failed to check if heroku remote is set')
    return True


def _success_message(heroku_app_name: str):
    """
    Print a success message
    """
    print(f'\n\ndash-tools: Successfully deployed to Heroku from git branch "heroku"!')
    print(
        f'dash-tools: To push changes, select the "Update Existing App" option after typing: dash-tools --heroku: deploy')
    print(
        f'dash-tools: Management Page: https://dashboard.heroku.com/apps/{heroku_app_name}')
    print(
        f'dash-tools: Application Page: https://{heroku_app_name}.herokuapp.com/')

    # Prompt user to open the deployed app
    if input('dash-tools: Enter any key to open in browser or q to exit > ') != 'q':
        webbrowser.open(f'https://{heroku_app_name}.herokuapp.com/')

    print('dash-tools: heroku: deploy: Finished')


def update_heroku_app(remote: str = 'heroku'):
    """
    Updates the existing heroku app

    Args:
        remote(str): Remote to update. Default 'heroku'
    """
    if not _add_changes_and_push_to_heroku('update'):
        exit('dash-tools: heroku: deploy: Failed to push to heroku')
    print('dash-tools: Changes pushed to heroku remote')


def _get_valid_app_name() -> str:
    """
    Returns a unique and valid heroku app name
    """
    heroku_app_name = herokuUtils.get_heroku_app_name()

    # Wait for user to input a correct name
    should_continue = False
    while not should_continue:
        # Check if the project already exists on Heroku if name is specified
        if not herokuUtils.check_heroku_app_name_available(heroku_app_name):
            print(
                f'dash-tools: App "{heroku_app_name}" already exists on Heroku!')
            print(
                'dash-tools: Please choose a unique name that isn\'t already taken.')
            heroku_app_name = herokuUtils.get_heroku_app_name()
        elif not herokuUtils.validate_heroku_app_name(heroku_app_name):
            print(
                f'dash-tools: App name "{heroku_app_name}" is not valid!')
            print('dash-tools: Heroku app names must start with a letter, end with a letter or digit, can only contain lowercase letters, numbers, and dashes, and have a minimum length of 3 characters.')
            heroku_app_name = herokuUtils.get_heroku_app_name()
        else:
            should_continue = True
    return heroku_app_name


def deploy_app_to_heroku(project_root_dir: os.PathLike):
    """
    Uses the Heroku CLI to deploy the current project
    """
    print('dash-tools: heroku: deploy: Starting')

    # Check if heroku CLI is installed
    if not herokuUtils.heroku_is_installed():
        print(f'dash-tools: Heroku CLI not installed!')
        print(f'dash-tools: See https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli')
        # Prompt user to open the deployed app
        if input('dash-tools: Enter any key to open in browser or q to exit > ') != 'q':
            webbrowser.open(
                'https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli')
        exit('dash-tools: heroku: deploy: Failed')

    # Check if git is installed
    if not gitUtils.git_is_installed():
        print(f'dash-tools: Git not installed!')
        print(f'dash-tools: See https://git-scm.com/downloads')
        # Prompt user to open the deployed app
        if input('dash-tools: Enter any key to open in browser or q to exit > ') != 'q':
            webbrowser.open('https://git-scm.com/downloads')
        exit('dash-tools: heroku: deploy: Failed')

    # Check that git is initialized in the current repo
    if not gitUtils.is_git_repository():
        print(f'dash-tools: Current directory is not a git repository!')
        # Prompt user to init git
        if prompt_user_choice('dash-tools: Would you like to init git?'):
            os.system('git init')
        else:
            print('dash-tools: To start a git repository, type: git init')
            exit('dash-tools: heroku: deploy: Failed')

    # Check that heroku remote is not already set
    if _check_heroku_remote_already_exists():
        print(f'dash-tools: Git remote "heroku" is already set!')
        print('dash-tools: Please choose an option below:')
        print('\t1. Push to the existing heroku remote (Update Existing App)')
        print('\t2. Remove the heroku remote and continue (Create New App)')
        print('\t3. Abort')
        while True:
            response = input('dash-tools: Choice (1, 2, 3) > ')
            if response == '1':
                update_heroku_app()
                exit('dash-tools: heroku: update: Success')
            elif response == '2':
                _remove_heroku_remote()
                break
            elif response == '3':
                exit('dash-tools: heroku: deploy: Aborted')
            else:
                pass

    # Get a unique app name
    heroku_app_name = _get_valid_app_name()

    # Check that the project has necessary files
    if not _check_required_files_exist(project_root_dir):
        print('dash-tools: Procfile, runtime.txt, and requirements.txt are needed for Heroku deployment.')
        exit('dash-tools: heroku: deploy: Aborted')

    # Check procfile is correct
    procfile = fileUtils.verify_procfile(project_root_dir)
    if not procfile['valid']:
        print(
            f'dash-tools: Procfile is incorrect. Did you include "{procfile["hook"]} = app.server" after instantiating "app = Dash(...)" in {procfile["dir"]}/{procfile["module"]}?')
        exit('dash-tools: heroku: deploy: Failed')

    # Log into Heroku
    if not herokuUtils.login_heroku_successful():
        print(f'dash-tools: Heroku login failed.')
        exit('dash-tools: heroku: deploy: Failed')

    # Confirm deployment settings and create the project on Heroku if the user confirms
    if not prompt_user_choice(f'dash-tools: Please confirm creating app {heroku_app_name} on Heroku and adding git remote "heroku".'):
        exit('dash-tools: heroku: deploy: Aborted')

    # Create the project on Heroku and capture the git remote URL
    if not herokuUtils.create_app_on_heroku(heroku_app_name):
        exit(
            f'dash-tools: heroku: deploy: Deploying app {heroku_app_name} to Heroku failed.')

    # Add python buildpack
    print(f'dash-tools: Adding python buildpack')
    os.system(f'heroku buildpacks:add heroku/python -a {heroku_app_name}')

    # Push to Heroku
    _add_changes_and_push_to_heroku(heroku_app_name)

    # Print success message and exit
    _success_message(heroku_app_name)
