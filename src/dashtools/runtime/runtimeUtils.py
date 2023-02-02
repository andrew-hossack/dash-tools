'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-05-23 00:08:07
 # @ Handle running the app
'''


import os
import subprocess
from typing import Union
from dashtools.data import configUtils
from dashtools.deploy import fileUtils


def _is_correct_python_command(command: str) -> bool:
    """
    Try running the python command
    Return True if it works, else False
    """
    try:
        subprocess.check_output(
            f'{command} --version',
            shell=True,
            stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def _try_all_commands() -> Union[str, None]:
    """
    Try all python commands
    Return the first one that works or None if none work
    """
    command = None
    for cmd in ['python', 'python3', 'python.exe', 'python3.exe']:
        if _is_correct_python_command(cmd):
            command = cmd
            break
    return command


def set_python_shell_cmd(command: str):
    """
    Set the python shell command
    """
    if _is_correct_python_command(command):
        configUtils.set_config_value('python_shell_cmd', command)
        print(
            f'dashtools: run: success: Python shell command set to {command}')
    else:
        print(
            f'dashtools: run: error: Command {command} is not valid for running Python')
    return


def _python_shell_cmd() -> str:
    """
    Get the python shell command
    """
    command = configUtils.get_config_value('python_shell_cmd')
    if not command:
        command = _try_all_commands()
        if command:
            configUtils.set_config_value('python_shell_cmd', command)
        else:
            print('dashtools: run: error: None of the following commands were found on your system: python, python.exe, python3, python3.exe')
            print('dashtools: run: Please set the python shell command with "dashtools run --set-python-shell-cmd <command>", or fall back to running your app from the app.py file')
            print('dashtools: View Troubleshooting docs for more info')
            exit(1)
    return command


def _run_from_app(root_path: os.PathLike):
    """
    Try looking for an app.py file in the directory recursively
    """
    # Find app.py file in the root_path director
    root = fileUtils.app_root_path(root_path)
    if not root:
        print('dashtools: run: No app.py file found')
        exit(1)
    try:
        print(
            f'dashtools: Running From {root + "/" if root else ""}app.py')
        os.chdir(root)
        # Has to run as os.system() to get the output
        # This means that if no app file is found, an error will be printed to screen
        # And cannot be handled in a cleaner way
        os.system(f'{_python_shell_cmd()} app.py')
        return
    except Exception:
        pass


def run_app(root_path: os.PathLike):
    '''
    Look for a Procfile to run the app, else recursive search for app.py file
    '''
    # Check Procfile exists
    if fileUtils.check_file_exists(root_path, 'Procfile'):
        proc = fileUtils.verify_procfile(root_path)
        if proc['valid']:
            print('dashtools: Running From Procfile')
            os.chdir(root_path)
            modpath = proc["dir"].replace("/", ".").replace("\\", ".")
            modname = proc["module"].replace(".py", "")
            os.system(f'{_python_shell_cmd()} -m {modpath}.{modname}')
        else:
            # Invalid Procfile, try running app.py
            _run_from_app(root_path)
    else:
        # No Procfile, try running app.py
        _run_from_app(root_path)
    return
