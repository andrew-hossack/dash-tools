'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-05-23 00:08:07
 # @ Handle running the app
 # TODO IMPLEMENT THIS FEATURE. This is a work in progress.
 # TODO Initially run through a list of python shell commands to figure
 # out how to run the app, e.g. python, python3, python.exe, etc. Save
 # to an environment variable. Else, prompt user to enter the command.
'''


import os
from dashtools.deploy.fileUtils import verify_procfile, check_file_exists


def _run_from_app(root_path: os.PathLike):
    """
    Try looking for an app.py file in the directory recursively
    """
    # Find app.py file in the root_path directory
    for root, _, files in os.walk(root_path):
        if 'app.py' in files:
            break
    try:
        print(
            f'dashtools: Running From {root + "/" if root else ""}app.py')
        os.chdir(root)
        # NOTE Not too sure if python3 is the right command for all systems, it might need to be changed
        os.system(f'python3 app.py')
        # Has to run as os.system() to get the output
        # This means that if no app file is found, an error will be printed to screen
        # And cannot be handled in a cleaner way
    except Exception:
        exit('dashtools: run: No app.py file found')


def run_app(root_path: os.PathLike):
    '''
    Look for a Procfile to run the app, else recursive search for app.py file
    # TODO verify this works for all systems. Not sure if python3 is correct cmd
    # TODO web: gunicorn --timeout 600 --chdir NRCCallApp/dashboard app:server DOES NOT WORK
    '''
    # Check Procfile exists
    if check_file_exists(root_path, 'Procfile'):
        # Look for a Procfile to run the app, else recursive search for app.py file
        proc = verify_procfile(root_path)
        if proc['valid']:
            print('dashtools: Running From Procfile')
            os.chdir(root_path)
            modpath = proc["dir"].replace("/", ".").replace("\\", ".")
            modname = proc["module"].replace(".py", "")
            # NOTE Not too sure if python3 is the right command for all systems, it might need to be changed
            os.system(f'python3 -m {modpath}.{modname}')
        else:
            _run_from_app(root_path)
    else:
        _run_from_app(root_path)
    return
