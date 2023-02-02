'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-05-22 22:21:30
 # @ Used to create new templates from a directory
'''

import os
import shutil

from dashtools.deploy import deployHeroku, fileUtils
from dashtools.templating import buildAppUtils


def create_template(src: os.PathLike, dest: os.PathLike):
    """
    Recursively copies all files and directories from src. Appends '.template' to all files.
    Saves new template to parent directory of src.
    """

    if not os.path.exists(src):
        print(f"dashtools: templates: init: Source file {src} does not exist")
        print('dashtools: templates: init: Failed')
        exit(1)

    # Check for file write permissions in the base directory (command invoke directory)
    if not buildAppUtils.check_write_permission(dest):
        print(
            f'dashtools: templates: init: No write permissions for {dest}')
        exit(f'dashtools: templates: init: Failed')

    # Create the new template directory
    src = os.path.join(src, '')
    template_base_dir = os.path.join(dest, f'{os.path.normpath(src)}Template')
    if os.path.exists(template_base_dir):
        print(
            f'dashtools: templates: init: Template directory {template_base_dir} already exists')
        exit(f'dashtools: templates: init: Failed')

    # Check Procfile exists
    if not fileUtils.check_file_exists(src, 'Procfile'):
        print(
            f'dashtools: templates: init: No Procfile found in {src}')
        if deployHeroku.prompt_user_choice("dashtools: templates: init: Create Procfile?"):
            fileUtils.create_procfile(src)

    # Verify procfile
    if not fileUtils.verify_procfile(src)["valid"]:
        print(
            f'dashtools: templates: init: Procfile in {src} is invalid')
        if not deployHeroku.prompt_user_choice("dashtools: Continue?"):
            exit(f'dashtools: templates: init: Aborted')

    # Check runtime exists
    if not fileUtils.check_file_exists(src, 'runtime.txt'):
        print(
            f'dashtools: templates: init: No runtime.py found in {src}')
        if deployHeroku.prompt_user_choice("dashtools: templates: init: Create runtime.py?"):
            fileUtils.create_runtime_txt(src)

    # Make the new template directory
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
    print(
        f'dashtools: templates: init: Created template {template_base_dir}')
