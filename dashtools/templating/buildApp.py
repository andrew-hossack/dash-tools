'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 13:57:48
 # Build dash apps with dashtools
'''

import datetime
import os
import shutil

from dashtools.templating import buildAppUtils


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


def create_app(target_dir: os.PathLike, app_name: str, template: buildAppUtils.Template):
    '''
    Create a new app in the target directory.

    Looks for files in the /template directory
    '''
    # Check arguments
    buildAppUtils.check_create_app_args(target_dir, app_name)

    # Check for file write permissions in the base directory (command invoke directory)
    if not buildAppUtils.check_write_permission(target_dir):
        print(
            f'dashtools: init: No write permissions for {target_dir}')
        exit(f'dashtools: init: Failed')

    # Copy files from template directory
    template_dir = os.path.join('templates', template.value)
    template_base_path = buildAppUtils.get_templates_data_path(template_dir)
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
            dest = os.path.join(target_dir, app_name, rel_path, name)
            dest = dest.replace('.template', '')
            dest = dest.replace(r'{appName}', app_name)

            # Create the directory if it doesn't exist
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))

            # Copy the file
            shutil.copyfile(src, dest)

            # Format the file
            _format_file(name, app_name, dest)

    print(
        f'dashtools: init: Created new app {app_name} at {os.path.join(target_dir, app_name)} with {template.name} template')
