'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-04 13:23:14
'''
import os
import random
import re
import string
import subprocess
import webbrowser
from typing import Union

import requests


def _heroku_is_installed() -> bool:
    """
    Check that heroku CLI is installed on the system
    Looks for "heroku/X.Y.Z " in the output of "heroku --version"
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


def _is_git_repository() -> bool:
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


def _check_file_exists(root_path: os.PathLike, file_name: str) -> bool:
    """
    Check that a file exists
    """
    path = os.path.join(root_path, file_name)
    if not os.path.exists(path):
        return False
    return True


def _create_requirements_txt(root_path: os.PathLike):
    """
    Creates requirements.txt file using pipreqs
    """
    print('dash-tools: deploy-heroku: Creating requirements.txt')
    os.system(f'pipreqs {root_path}')
    # Append gunicorn to requirements.txt
    with open(os.path.join(root_path, 'requirements.txt'), 'a') as requirements_file:
        requirements_file.write('gunicorn')


def _create_runtime_txt(root_path: os.PathLike):
    """
    Create runtime.txt file
    Default behavior is to use python-3.8.10
    """
    with open(os.path.join(root_path, 'runtime.txt'), 'w') as runtime_file:
        runtime_file.write('python-3.8.10')
    print('dash-tools: deploy-heroku: Created runtime.txt using python-3.8.10')


def _create_procfile(root_path: os.PathLike):
    """
    Create a procfile but prompt the user to verify it before continuing.
    """
    with open(os.path.join(root_path, 'Procfile'), 'w') as procfile:
        procfile.write(
            f'web: gunicorn --timeout 600 --chdir src app:server')
    print(f'dash-tools: deploy-heroku: Created Procfile')


def _check_heroku_app_name_available(heroku_app_name: str) -> bool:
    """
    Check that the app name is available on Heroku

    Returns:
        True if available
        False if not
    """
    try:
        if requests.get(f'https://{heroku_app_name}.herokuapp.com/', headers={'User-Agent': 'Custom'}).status_code == 404:
            return True
    except requests.exceptions.ConnectionError:
        exit('dash-tools: deploy-heroku: Invalid Heroku app name')
    return False


def _verify_procfile(root_path: os.PathLike) -> dict:
    """
    Verifies that the Procfile is correct:

    Ex. If "... --chdir src app:server ..." is in Procfile, check that
        'server' hook exists in src/app.py

    Returns:
        {
            'valid': True (valid) or False (invalid),
            'dir': Directory of app,
            'hook': Hook name
            'module': Module name
        }
    """
    with open(os.path.join(root_path, 'Procfile'), 'r') as procfile:
        procfile_contents = procfile.read()

    # Look for --chdir somedir
    chdir_regex = r"--chdir [a-zA-Z]+"
    try:
        chdir = re.search(chdir_regex, procfile_contents).group(0)
        chdir = chdir.replace('--chdir ', '')
    except (AttributeError, IndexError):
        chdir = ''

    # Look for module:hook
    hook_regex = r"[a-zA-Z]+:[a-zA-Z]+"
    try:
        hook = re.search(hook_regex, procfile_contents).group(0)
        hook_module = hook.split(':')[0] + '.py'
        hook = hook.split(':')[1]
    except (AttributeError, IndexError):
        hook = ''
        return {
            'valid': False,
            'dir': chdir,
            'hook': hook,
            'module': hook_module
        }

    modpath = os.path.join(root_path, chdir, hook_module)

    # Check that the module exists
    if not os.path.exists(modpath):
        return {
            'valid': False,
            'dir': chdir,
            'hook': hook,
            'module': hook_module
        }

    # Check that the hook exists in the module
    with open(modpath, 'r') as modfile:
        modfile_contents = modfile.read()

    # Look for the hook "{hook} =" or "{hook}=" with spaces and newlines
    hook_regex = f"^([\n]+{hook}\s=|[\n]+{hook}=|{hook}=|{hook}\s=)"
    try:
        re.search(hook_regex, modfile_contents, re.MULTILINE).group(0)
        return {
            'valid': True,
            'dir': chdir,
            'hook': hook,
            'module': hook_module
        }
    except (AttributeError, IndexError) as e:
        return {
            'valid': False,
            'dir': chdir,
            'hook': hook,
            'module': hook_module
        }


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


def _check_required_files_exist(root_path: os.PathLike) -> bool:
    """
    Check for Procfile, runtime.txt, requirements.txt
    """
    deploy_should_continue = True
    # Check if procfile exists
    if not _check_file_exists(root_path, 'Procfile'):
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file Procfile not found. Create one automatically?'):
            _create_procfile(root_path)
        else:
            deploy_should_continue = False
    # Check for the Runtime file
    if (not _check_file_exists(root_path, 'runtime.txt')) and deploy_should_continue:
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file runtime.txt not found. Create one automatically?'):
            _create_runtime_txt(root_path)
        else:
            deploy_should_continue = False
    # Check for the Requirements file
    if (not _check_file_exists(root_path, 'requirements.txt')) and deploy_should_continue:
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file requirements.txt not found. Create one automatically?'):
            _create_requirements_txt(root_path)
        else:
            deploy_should_continue = False
    return deploy_should_continue


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


def _create_app_on_heroku(app_name: str) -> bool:
    """
    Create the project on Heroku and return the git remote URL

    Returns:
        Success of the operation (True/False)
    """
    print(f'dash-tools: deploy-heroku: Creating {app_name} on Heroku')
    url_regex = r'https:\/\/git\.heroku\.com\/[a-zA-Z0-9-_]*\.git'
    try:
        heroku_command_output = subprocess.check_output(
            f'heroku create {app_name}', shell=True)
        git_remote_url = re.search(
            url_regex, heroku_command_output.decode('utf-8'))
        try:
            git_remote_url.group(0)
        except AttributeError:
            # No url found. Something is wrong
            return False
    except subprocess.CalledProcessError:
        return False
    return True


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


def _remove_heroku_remote():
    """
    Remove the heroku remote

    Returns:
        True if successful
        False if failed
    """
    print('dash-tools: deploy-heroku: Removing heroku remote')
    try:
        subprocess.check_output('git remote rm heroku', shell=True)
    except subprocess.CalledProcessError:
        exit('dash-tools: deploy-heroku: Failed to remove heroku remote')


def _success_message(heroku_app_name: str):
    """
    Print a success message
    """
    print(f'\n\ndash-tools: deploy-heroku: Successfully deployed to Heroku!')
    print(
        f'dash-tools: deploy-heroku: Published to git remote: "heroku". Make changes with the "git push heroku" command.')
    print(
        f'dash-tools: deploy-heroku: Management Page: https://dashboard.heroku.com/apps/{heroku_app_name}')
    print(
        f'dash-tools: deploy-heroku: Application Page: https://{heroku_app_name}.herokuapp.com/')

    # Prompt user to open the deployed app
    if input('dash-tools: deploy-heroku: Enter any key to open in browser or q to exit > ') != 'q':
        webbrowser.open(f'https://{heroku_app_name}.herokuapp.com/')


def _get_heroku_app_name():
    """
    Create or generate app name if one isn't provided
    """
    print('dash-tools: deploy-heroku: No app name provided. Please type a unique name or press enter to generate one automatically.')
    app_name = input('dash-tools: App Name (Optional) > ')
    if app_name == '':
        # Generate a random app name
        app_name = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=12))
        # App names must start with letter. Use 'dt-' for dash-tools
        app_name = ''.join(('dt-', app_name))
    print(f'dash-tools: deploy-heroku: Using app name "{app_name}"')
    return app_name


def deploy_app_to_heroku(project_root_dir: os.PathLike, heroku_app_name: Union[str, None]):
    """
    Uses the Heroku CLI to deploy the current project
    """
    print('dash-tools: deploy-heroku: Starting')

    # Check if heroku CLI is installed
    if not _heroku_is_installed():
        print(f'dash-tools: deploy-heroku: Heroku CLI not installed!')
        print(f'dash-tools: deploy-heroku: See https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli')
        exit('dash-tools: deploy-heroku: Failed')

    # Check if git is installed
    if not _git_is_installed():
        print(f'dash-tools: deploy-heroku: Git not installed!')
        print(f'dash-tools: deploy-heroku: See https://git-scm.com/downloads')
        exit('dash-tools: deploy-heroku: Failed')

    # Check that git is initialized in the current repo
    if not _is_git_repository():
        print(f'dash-tools: deploy-heroku: Current directory is not a git repository!')
        print(
            f'dash-tools: deploy-heroku: Did you forget to "git init"? See https://git-scm.com/docs/git-init')
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

    # Generate or let user type in app name if it is not provided
    if not heroku_app_name:
        heroku_app_name = _get_heroku_app_name()

    # Check if the project already exists on Heroku if name is specified
    if not _check_heroku_app_name_available(heroku_app_name):
        print(
            f'dash-tools: deploy-heroku: App "{heroku_app_name}" already exists on Heroku!')
        print(
            'dash-tools: deploy-heroku: Please choose a unique name that isn\'t already taken.')
        exit('dash-tools: deploy-heroku: Failed')

    # Check that the project has necessary files
    if not _check_required_files_exist(project_root_dir):
        print('dash-tools: deploy-heroku: Procfile, runtime.txt, and requirements.txt are needed for Heroku deployment.')
        exit('dash-tools: deploy-heroku: Aborted')

    # Check procfile is correct
    procfile = _verify_procfile(project_root_dir)
    if not procfile['valid']:
        print(
            f'dash-tools: deploy-heroku: Procfile is incorrect. Did you include "{procfile["hook"]} = app.server" after instantiating "app = Dash(...)" in {procfile["dir"]}/{procfile["module"]}?')
        print(
            'dash-tools: deploy-heroku: See https://devcenter.heroku.com/articles/procfile')
        exit('dash-tools: deploy-heroku: Failed')

    # Log into Heroku
    if not _login_heroku_successful():
        print(f'dash-tools: deploy-heroku: Heroku login failed.')
        exit('dash-tools: deploy-heroku: Failed')

    # Confirm deployment settings and create the project on Heroku if the user confirms
    if not _prompt_user_choice(f'dash-tools: deploy-heroku: Please confirm creating app {heroku_app_name} on Heroku and adding git remote "heroku".'):
        exit('dash-tools: deploy-heroku: Aborted')

    # Create the project on Heroku and capture the git remote URL
    if not _create_app_on_heroku(heroku_app_name):
        exit(
            f'dash-tools: deploy-heroku: Deploying app {heroku_app_name} to Heroku failed.')

    # Add python buildpack
    print(f'dash-tools: deploy-heroku: Adding python buildpack')
    os.system(f'heroku buildpacks:add heroku/python -a {heroku_app_name}')

    # Push to Heroku
    _add_changes_and_push_to_heroku(heroku_app_name)

    # Print success message and exit
    _success_message(heroku_app_name)
