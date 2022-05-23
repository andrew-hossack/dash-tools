'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-05-22 22:21:30
 # @ Used to create new templates from a directory
'''

import os
import shutil

from dash_tools.templating import buildAppUtils


def create_template(src: os.PathLike, dest: os.PathLike):
    """
    Recursively copies all files and directories from src. Appends '.template' to all files.
    Saves new template to parent directory of src.
    """

    # Check for file write permissions in the base directory (command invoke directory)
    if not buildAppUtils.check_write_permission(dest):
        print(
            f'dash-tools: templates: init: No write permissions for {dest}')
        exit(f'dash-tools: templates: init: Failed')

    # Create the new template directory
    src = os.path.join(src, '')
    template_base_dir = os.path.join(dest, f'{os.path.normpath(src)}Template')
    if os.path.exists(template_base_dir):
        print(
            f'dash-tools: templates: init: Template directory {template_base_dir} already exists')
        exit(f'dash-tools: templates: init: Failed')
    os.mkdir(template_base_dir)

    # Copy files from src to template_base_dir, appending '.template' to all files
    for path, _, files in os.walk(src):
        for name in files:
            # Skip already .template files
            if('.template' in name):
                continue

            # Get the relative path to the file
            relative_path = os.path.relpath(
                path, src)
            rel_src = os.path.join(path, name)

            # Get the destination path
            rel_dest = relative_path if relative_path != '.' else ''
            dest = os.path.join(
                template_base_dir,
                rel_dest,
                name +
                '.template')

            # Create the directory if it doesn't exist
            if not os.path.exists(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))

            # Copy the file
            shutil.copyfile(rel_src, dest)
