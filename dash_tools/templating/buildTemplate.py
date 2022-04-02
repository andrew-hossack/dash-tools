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
from .templateUtils import _check_create_app_args, _convert_to_template_or_error, _get_templates_data_path, Templates


def create_app(base_dir: os.PathLike, app_name: str, use_template: Union[Templates, str]):
    '''
    Create a new app in the target directory.

    Looks for files in the /template directory
    '''
    # Check arguments
    _check_create_app_args(base_dir, app_name)
    use_template = _convert_to_template_or_error(use_template)

    print(
        f'dash-tools: init: creating new app {app_name} at {base_dir} with template {use_template}')

    # Copy files from template directory
    template = os.path.join('templates', use_template.value)
    for path, _, files in os.walk(_get_templates_data_path(template)):
        for name in files:
            # Skip non .template files
            if('.template' not in name):
                continue

            # Get the relative path to the file
            relative_path = os.path.relpath(
                path, _get_templates_data_path(template))
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

            # Replace {appName} and {createTime} in .py and .md files
            if('.py' in name or '.md' in name):
                with open(dest, 'r') as f:
                    content = f.read()
                    content = content.replace(r'{appName}', app_name)
                    content = content.replace(
                        r'{createTime}', str(datetime.datetime.now()))
                    with open(dest, 'w') as f:
                        f.write(content)
