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


def _create_procfile(root_path: os.PathLike, app_name: str):
    """
    Create a procfile but prompt the user to verify it before continuing.
    """
    with open(os.path.join(root_path, 'Procfile'), 'w') as procfile:
        procfile.write(
            f'web: gunicorn --timeout 600 --chdir {app_name} app:server')
    print(f'dash-tools: deploy-heroku: Created Procfile')


def _prompt_user_choice(message: str) -> bool:
    """
    Prompt the user to continue or not.

    Returns:
        True (y/Y)
        False (n/N)
    """
    print(message)
    response = input('dash-tools: Continue? (y/n) > ')
    if response.lower() == 'y':
        return True
    elif response.lower() == 'n':
        return False
    else:
        return _prompt_user_choice(message)


def _check_required_files(root_path: os.PathLike) -> bool:
    """
    Check for Procfile, runtime.txt, requirements.txt
    """
    print(f'dash-tools: deploy-heroku: Checking for Procfile, runtime.txt, and requirements.txt')
    deploy_should_continue = True
    if not _check_file_exists(root_path, 'Procfile'):
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file Procfile not found. Create one automatically?'):
            # HOTFIX / TODO / TEMP
            # We will infer the name of the directory that the app.py file is located.
            # Assume that the project is <MyApp>/<MyApp>/app.py. Since we only know the top-level
            # directory as root_path (<MyApp>/.../app.py), we will infer that app.py is in root_path/root_path/app.py
            app_dir = os.path.basename(root_path)
            if _prompt_user_choice(
                    f'dash-tools: deploy-heroku: Verify that "server = app.server" is declared in {app_dir}/app.py! See https://devcenter.heroku.com/articles/procfile'):
                _create_procfile(root_path, app_dir)
            else:
                deploy_should_continue = False
        else:
            deploy_should_continue = False
    if (not _check_file_exists(root_path, 'runtime.txt')) and deploy_should_continue:
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file runtime.txt not found. Create one automatically?'):
            _create_runtime_txt(root_path)
        else:
            deploy_should_continue = False
    if (not _check_file_exists(root_path, 'requirements.txt')) and deploy_should_continue:
        if _prompt_user_choice(
                'dash-tools: deploy-heroku: Required file requirements.txt not found. Create one automatically?'):
            _create_requirements_txt(root_path)
        else:
            deploy_should_continue = False
    return deploy_should_continue


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


def deploy_app_to_heroku(project_root_dir: os.PathLike, heroku_app_name: str):
    """
    Uses the Heroku CLI to deploy the current project
    """
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

    # Check that the project has necessary files
    if not _check_required_files(project_root_dir):
        print('dash-tools: deploy-heroku: Procfile, runtime.txt, and requirements.txt are needed for Heroku deployment.')
        exit('dash-tools: deploy-heroku: Aborted')

    # Log into Heroku
    if not _login_heroku_successful():
        print(f'dash-tools: deploy-heroku: Failed to log into Heroku!')
        exit('dash-tools: deploy-heroku: Failed')

    # Confirm deployment settings and create the project on Heroku if the user confirms
    if not _prompt_user_choice(f'dash-tools: deploy-heroku: Please confirm creating app "{heroku_app_name}" on Heroku and adding git remote "heroku".'):
        exit('dash-tools: deploy-heroku: Aborted')

    # Create the project on Heroku and capture the git remote URL
    if not _create_app_on_heroku(heroku_app_name):
        exit(
            f'dash-tools: deploy-heroku: Deploying app {heroku_app_name} to Heroku failed. Check that the app name is valid.')

    # Add python buildpack
    print(f'dash-tools: deploy-heroku: Adding python buildpack')
    os.system(f'heroku buildpacks:add heroku/python -a {heroku_app_name}')

    # Create a commit to push to Heroku
    print(f'dash-tools: deploy-heroku: Creating commit to push to Heroku')
    os.system(f'git add .')
    os.system(
        f'git commit -m "Initial deploy to heroku for {heroku_app_name}"')

    # Push to Heroku
    print(f'dash-tools: deploy-heroku: Pushing to Heroku')
    os.system(f'git push heroku master')

    print(
        f'dash-tools: deploy-heroku: Published to git remote: "heroku" on branch "master". Push changes to this branch!')
    print(f'dash-tools: deploy-heroku: Successfully deployed to Heroku!')
    print(
        f'dash-tools: deploy-heroku: Management Page https://dashboard.heroku.com/apps/{heroku_app_name}')
    print(
        f'dash-tools: deploy-heroku: Deployed to https://{heroku_app_name}.herokuapp.com/')
    print(f'dash-tools: deploy-heroku: Finished!')
