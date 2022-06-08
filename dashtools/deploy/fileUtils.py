'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 11:46:39
 # File util functions
'''
import os
import re
import subprocess
from typing import Union


def check_file_exists(root_path: os.PathLike, file_name: str) -> bool:
    """
    Check that a file exists
    """
    path = os.path.join(root_path, file_name)
    if not os.path.exists(path):
        return False
    return True


def _add_requirement(root_path: os.PathLike, requirement: str):
    """
    Adds a requirement to the requirements.txt file if it doesn't already exist
    """
    # Append gunicorn to requirements.txt
    with open(os.path.join(root_path, 'requirements.txt'), 'r+') as requirements_file:
        if requirement not in requirements_file.read():
            requirements_file.write(f'{requirement}\n')


def create_requirements_txt(root_path: os.PathLike, update=False):
    """
    Creates requirements.txt file using pipreqs
    """
    print(
        f'dashtools: {"Updating" if update else "Creating"} requirements.txt')
    try:
        if update:
            subprocess.check_output(
                f'pipreqs --force {root_path}', shell=True)
        else:
            subprocess.check_output(
                f'pipreqs {root_path}', shell=True)
    except subprocess.CalledProcessError:
        # pipreqs throws a SyntaxError if it encounters a non-ASCII character
        # One reason may be that the user is not in a valid dash app directory
        print('dashtools: Error creating requirements.txt')
        print('dashtools: Did you run heroku --deploy in a valid dash app directory?')
        exit('dashtools: heroku: deploy: Failed')

    # Add requirements that might not be in requirements.txt
    for req in ['gunicorn', 'pandas']:
        _add_requirement(root_path, req)


def create_runtime_txt(root_path: os.PathLike):
    """
    Create runtime.txt file
    Default behavior is to use python-3.8.10
    """
    with open(os.path.join(root_path, 'runtime.txt'), 'w') as runtime_file:
        runtime_file.write('python-3.8.10')
    print('dashtools: Created runtime.txt using python-3.8.10')


def app_root_path(root_path: os.PathLike) -> Union[os.PathLike, None]:
    """
    Look for an app.py file in the directory recursively

    Returns:
        Path to app.py file if found, else None
    """
    # Find app.py file in the root_path directory
    app_path = None
    for root, _, files in os.walk(root_path):
        if 'app.py' in files:
            app_path = root
            break
    return app_path


def create_procfile(root_path: os.PathLike):
    """
    Create a procfile but prompt the user to verify it before continuing.
    """
    app_path = app_root_path(root_path)
    rel_path = os.path.relpath(app_path, root_path)
    chdir = f'{" --chdir " + rel_path if rel_path != "." else ""}'
    with open(os.path.join(root_path, 'Procfile'), 'w') as procfile:
        procfile.write(
            f'web: gunicorn{chdir if len(chdir) > 0 else ""} app:server')
    print(f'dashtools: Created Procfile')


def verify_procfile(root_path: os.PathLike) -> dict:
    """
    Verifies that the Procfile is correct:

    Ex. If "... --chdir src app:server ..." is in Procfile, check that
        'server' hook exists in src/app.py

    Returns:
        {
            'valid': True (valid) or False (invalid),
            'dir': Directory of app,
            'module': Module name
            'hook': Hook name
        }
    """
    with open(os.path.join(root_path, 'Procfile'), 'r', encoding="utf8") as procfile:
        procfile_contents = procfile.read()

    # Look for --chdir somedir
    chdir_regex = r"--chdir [a-zA-Z\/\\]+"
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
    with open(modpath, 'r', encoding="utf8") as modfile:
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
    except (AttributeError, IndexError):
        return {
            'valid': False,
            'dir': chdir,
            'hook': hook,
            'module': hook_module
        }
