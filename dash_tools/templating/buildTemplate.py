'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 13:57:48
 # Build dash apps with dash-tools
'''

import datetime
import os
import shutil
import datetime
from typing import Union
from dash_tools.templating import templateUtils


def _format_file(name: os.PathLike, app_name: str, dest: os.PathLike):
    """
    Look for files ending in .py, .md, Procfile, and format them

    Change {appName} to the app name
    Change {createTime} to the current time

    Modifies the user's file in place
    """
    if('.py' in name or '.md' in name or 'Procfile' in name):
        with open(dest, 'r') as f:
            content = f.read()
            content = content.replace(r'{appName}', app_name)
            content = content.replace(
                r'{createTime}', str(datetime.datetime.now()))
            with open(dest, 'w') as f:
                f.write(content)


def _check_write_permission(path: os.PathLike) -> bool:
    """
    Check for write permission in directory/

    Returns:
        True if write access else allowed False
    """
    return os.access(path, os.W_OK)


def create_app(base_dir: os.PathLike, app_name: str, use_template: Union[templateUtils.Template, str]):
    '''
    Create a new app in the target directory.

    Looks for files in the /template directory
    '''
    # Check arguments
    templateUtils.check_create_app_args(base_dir, app_name)
    use_template = templateUtils.convert_to_template_or_error(use_template)
    print(
        f'dash-tools: init: Creating new app "{app_name}" at {os.path.join(base_dir, app_name)} using {use_template}')

    # Check for file write permissions in the base directory (command invoke directory)
    if not _check_write_permission(base_dir):
        print(
            f'dash-tools: init: No write permissions for {base_dir}')
        exit(f'dash-tools: init: Failed')

    # Copy files from template directory
    template = os.path.join('templates', use_template.value)
    template_base_path = templateUtils.get_templates_data_path(template)
    for path, _, files in os.walk(template_base_path):
        for name in files:
            # Skip non .template files
            if('.template' not in name):
                continue

            # Get the relative path to the file
            relative_path = os.path.relpath(
                path, template_base_path)
            src = os.path.join(path, name)

            # Get the destination path
            rel_path = relative_path if relative_path != '.' else ''
            dest = os.path.join(base_dir, app_name, rel_path, name)
            dest = dest.replace('.template', '')
            dest = dest.replace(r'{appName}', app_name)

            # Create the directory if it doesn't exist
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))

            # Copy the file
            shutil.copyfile(src, dest)

            # Format the file
            _format_file(name, app_name, dest)

    print(f'dash-tools: init: Finished')
