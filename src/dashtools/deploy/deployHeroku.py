'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:23:14
'''
import os
import re
import subprocess
import webbrowser

from dashtools.deploy import fileUtils, gitUtils, herokuUtils


def _handle_heroku_files(root_path: os.PathLike) -> bool:
    """
    Check for Procfile, runtime.txt, requirements.txt
    """
    procfile_exists = fileUtils.check_file_exists(root_path, 'Procfile')
    runtime_exists = fileUtils.check_file_exists(root_path, 'runtime.txt')
    requirements_exists = fileUtils.check_file_exists(
        root_path, 'requirements.txt')

    if not procfile_exists:
        if prompt_user_choice('dashtools: Required file Procfile not found. Create one automatically?'):
            fileUtils.create_procfile(root_path)
            procfile_exists = True

    if not runtime_exists:
        if prompt_user_choice('dashtools: Required file runtime.txt not found. Create one automatically?'):
            fileUtils.create_runtime_txt(root_path)
            runtime_exists = True

    if not requirements_exists:
        if prompt_user_choice('dashtools: Required file requirements.txt not found. Create one automatically?'):
            fileUtils.create_requirements_txt(root_path, update=False)
            requirements_exists = True
    else:
        # Update requirements.txt
        fileUtils.create_requirements_txt(root_path, update=True)

    if not (procfile_exists and runtime_exists and requirements_exists):
        print('dashtools: Procfile, runtime.txt, and requirements.txt are needed for Heroku deployment.')
        print('dashtools: heroku: deploy: Aborted')
        exit(1)


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
    response = input(f'dashtools: {prompt}')
    if response.lower() == 'y':
        return True
    elif response.lower() == 'n':
        return False
    elif does_repeat:
        return prompt_user_choice(message)
    else:
        return False


def _add_changes_and_push_to_heroku(heroku_app_name: str, remote: str = 'heroku') -> bool:
    """
    Add changes to the repository and push to Heroku

    Returns:
        True (Success)
        False (Failure)
    """
    # Create a commit to push to Heroku
    try:
        subprocess.check_output(f'git add .', shell=True)
        print(f'dashtools: Created commit to push to {remote}')
        subprocess.check_output(
            f'git commit -m "Deploy to Heroku for app {heroku_app_name} - dashtools"', shell=True)
        # Push to Heroku
        print(f'dashtools: Pushing to Heroku')
        subprocess.check_output(f'git push {remote} HEAD:master', shell=True)
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
    print('dashtools: Removing existing heroku remote')
    try:
        subprocess.check_output('git remote rm heroku', shell=True)
    except subprocess.CalledProcessError:
        print('dashtools: heroku: deploy: Failed to remove heroku remote')
        exit(1)


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
        print('dashtools: heroku: deploy: Failed to check if heroku remote is set')
        exit(1)
    return True


def _success_message(heroku_app_name: str):
    """
    Print a success message
    """
    print(f'\n\ndashtools: Successfully deployed to Heroku from git branch "heroku"!')
    print(
        f'dashtools: To push changes, select the "Update Existing App" option after typing: dashtools --heroku: deploy')
    print(
        f'dashtools: Management Page: https://dashboard.heroku.com/apps/{heroku_app_name}')
    print(
        f'dashtools: Application Page: https://{heroku_app_name}.herokuapp.com/')

    # Prompt user to open the deployed app
    if input('dashtools: Enter any key to open in browser or q to exit > ') != 'q':
        webbrowser.open(f'https://{heroku_app_name}.herokuapp.com/')

    print('dashtools: heroku: deploy: Finished')


def update_heroku_app(project_root: os.PathLike, remote: str = 'heroku'):
    """
    Updates the existing heroku app

    Args:
        remote(str): Remote to update. Default 'heroku'
    """
    # (Re)generate requirements file
    if fileUtils.check_file_exists(project_root, 'requirements.txt'):
        fileUtils.create_requirements_txt(project_root, update=True)
    if not _add_changes_and_push_to_heroku('update', remote=remote):
        print(f'dashtools: Unable to update heroku app. Project must be deployed to heroku before updating.')
        print('dashtools: heroku: update: Failed')
        exit(1)
    print('dashtools: Changes pushed to {remote} remote')
    print('dashtools: heroku: update: Success')
    exit(0)


def _get_valid_app_name() -> str:
    """
    Returns a unique and valid heroku app name
    """
    should_loop = True
    while should_loop:
        # Generate new name
        heroku_app_name = herokuUtils.get_heroku_app_name()
        # Check if the project already exists on Heroku if name is specified
        if not herokuUtils.check_heroku_app_name_available(heroku_app_name):
            print(
                f'dashtools: App "{heroku_app_name}" already exists on Heroku!')
            print('dashtools: Please choose a unique name that isn\'t already taken.')
        # Validate app name
        elif not herokuUtils.validate_heroku_app_name(heroku_app_name):
            print(
                f'dashtools: App name "{heroku_app_name}" is not valid!')
            print('dashtools: Heroku app names must start with a letter, end with a letter or digit, can only contain lowercase letters, numbers, and dashes, and have a minimum length of 3 characters and maximum length of 30 characters.')
        else:
            should_loop = False
    return heroku_app_name


def deploy_app_to_heroku(project_root_dir: os.PathLike):
    """
    Uses the Heroku CLI to deploy the current project
    """
    print('dashtools: heroku: deploy: Starting')

    # Check if heroku CLI is installed
    if not herokuUtils.heroku_is_installed():
        print(f'dashtools: Heroku CLI not installed!')
        print(f'dashtools: See https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli')
        # Prompt user to open the deployed app
        if input('dashtools: Enter any key to open in browser or q to exit > ') != 'q':
            webbrowser.open(
                'https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli')
        print('dashtools: heroku: deploy: Failed')
        exit(1)

    # Check if git is installed
    if not gitUtils.git_is_installed():
        print(f'dashtools: Git not installed!')
        print(f'dashtools: See https://git-scm.com/downloads')
        # Prompt user to open the deployed app
        if input('dashtools: Enter any key to open in browser or q to exit > ') != 'q':
            webbrowser.open('https://git-scm.com/downloads')
        print('dashtools: heroku: deploy: Failed')
        exit(1)

    # Check that git is initialized in the current repo
    if not gitUtils.is_git_repository():
        print(f'dashtools: A git repository is needed for deployment. Current directory is not a git repository!')
        # Prompt user to init git
        if prompt_user_choice('dashtools: Would you like to init git?'):
            os.system('git init')
        else:
            print('dashtools: To start a git repository, type: git init')
            print('dashtools: heroku: deploy: Failed')
            exit(1)

    # Check that heroku remote is not already set
    if _check_heroku_remote_already_exists():
        print(f'dashtools: Git remote "heroku" is already set!')
        print('dashtools: Please choose an option below:')
        print('\t1. Push to the existing heroku remote (Update Existing App)')
        print('\t2. Remove the heroku remote and continue (Create New App)')
        print('\t3. Abort')
        while True:
            response = input('dashtools: Choice (1, 2, 3) > ')
            if response == '1':
                update_heroku_app(project_root_dir)
            elif response == '2':
                _remove_heroku_remote()
                break
            elif response == '3':
                print('dashtools: heroku: deploy: Aborted')
                exit(1)
            else:
                pass

    # Check app.py file exists
    if not fileUtils.app_root_path(project_root_dir):
        print(f'dashtools: No app.py file found! An app.py file is required to deploy your app.')
        print('dashtools: heroku: deploy: Failed')
        exit(1)

    # Check that the project has necessary files, and generate them if not
    _handle_heroku_files(project_root_dir)

    # Get a unique app name
    heroku_app_name = _get_valid_app_name()

    # Check procfile is correct
    procfile = fileUtils.verify_procfile(project_root_dir)
    if not procfile['valid']:
        print(f'dashtools: Invalid Procfile!')
        print(
            f'dashtools: Did you include "{procfile["hook"]} = app.server" after instantiating "app = Dash(...)" in {procfile["dir"]}/{procfile["module"]}?')
        if not prompt_user_choice('dashtools: App will not start without a valid Procfile. Continuing is not recommended.'):
            print('dashtools: heroku: deploy: Aborted')
            exit(1)

    # Log into Heroku
    if not herokuUtils.login_heroku_successful():
        print(f'dashtools: Heroku login failed.')
        print('dashtools: heroku: deploy: Failed')
        exit(1)

    # Confirm deployment settings and create the project on Heroku if the user confirms
    if not prompt_user_choice(f'dashtools: Please confirm creating app {heroku_app_name} on Heroku and adding git remote "heroku".'):
        print('dashtools: heroku: deploy: Aborted')
        exit(1)

    # Create the project on Heroku and capture the git remote URL
    if not herokuUtils.create_app_on_heroku(heroku_app_name):
        print(
            f'dashtools: heroku: deploy: Deploying app {heroku_app_name} to Heroku failed.')
        exit(1)

    # Add python buildpack
    print(f'dashtools: Adding python buildpack')
    os.system(f'heroku buildpacks:add heroku/python -a {heroku_app_name}')

    # Push to Heroku
    _add_changes_and_push_to_heroku(heroku_app_name)

    # Print success message and exit
    _success_message(heroku_app_name)
