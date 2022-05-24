'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 11:46:39
 # File util functions
'''
import os
import re
import subprocess


def check_file_exists(root_path: os.PathLike, file_name: str) -> bool:
    """
    Check that a file exists
    """
    path = os.path.join(root_path, file_name)
    if not os.path.exists(path):
        return False
    return True


def create_requirements_txt(root_path: os.PathLike):
    """
    Creates requirements.txt file using pipreqs
    """
    print('dashtools: deploy-heroku: Creating requirements.txt')
    try:
        subprocess.check_output(f'pipreqs {root_path}', shell=True)
    except subprocess.CalledProcessError:
        # pipreqs throws a SyntaxError if it encounters a non-ASCII character
        # One reason may be that the user is not in a valid dash app directory
        print(
            f'dashtools: deploy-heroku: Error creating requirements.txt')
        print('dashtools: deploy-heroku: Did you run --deploy-heroku in a valid dash app directory?')
        exit('dashtools: deploy-heroku: Failed')
    # Append gunicorn to requirements.txt
    with open(os.path.join(root_path, 'requirements.txt'), 'a') as requirements_file:
        requirements_file.write('gunicorn')


def create_runtime_txt(root_path: os.PathLike):
    """
    Create runtime.txt file
    Default behavior is to use python-3.8.10
    """
    with open(os.path.join(root_path, 'runtime.txt'), 'w') as runtime_file:
        runtime_file.write('python-3.8.10')
    print('dashtools: deploy-heroku: Created runtime.txt using python-3.8.10')


def create_procfile(root_path: os.PathLike):
    """
    Create a procfile but prompt the user to verify it before continuing.
    """
    with open(os.path.join(root_path, 'Procfile'), 'w') as procfile:
        procfile.write(
            f'web: gunicorn --timeout 600 --chdir src app:server')
    print(f'dashtools: deploy-heroku: Created Procfile')


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
    except (AttributeError, IndexError):
        return {
            'valid': False,
            'dir': chdir,
            'hook': hook,
            'module': hook_module
        }
