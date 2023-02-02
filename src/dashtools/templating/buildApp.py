'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 13:57:48
 # Build dash apps with dashtools
'''
import datetime
import os
import shutil
import subprocess
import sys
from typing import Union

import pkg_resources
from dash import html

from dashtools.deploy import deployHeroku
from dashtools.templating import Templates, buildApp, buildAppUtils


def _check_pip_installed() -> bool:
    """
    Check if pip is installed
    """
    try:
        subprocess.check_output(
            'pip --version',
            shell=True,
            stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def _install_pip_requirement(requirement: str):
    '''
    Install a pip requirement
    '''
    print(f'dashtools: Installing {requirement}')
    os.system(f'pip install {requirement}')


def _check_pip_requirement_installed(requirement: str) -> bool:
    '''
    Check if a pip requirement is installed
    '''
    try:
        pkg_resources.get_distribution(requirement)
    except pkg_resources.DistributionNotFound:
        return False
    except pkg_resources.VersionConflict:
        return False
    return True


def _check_pip_requirements(requirements: list, template_value: str):
    '''
    Check if pip requirements are installed
    '''
    for req in requirements:
        if not _check_pip_requirement_installed(req):
            print(
                f'dashtools: Template {template_value} requires pip module {req}, which is not installed')
            if _check_pip_installed():
                if deployHeroku.prompt_user_choice(f'dashtools: Install {req}?'):
                    _install_pip_requirement(req)
                    print()
            else:
                print(f'dashtools: Please install {req} manually')


def _get_template_required_packages(template_value: str) -> list:
    """
    Looks for 'packages' file in template directory. If one is found,
    return a list of pip requirements.
    """
    packages_file = os.path.join(
        buildApp.get_template_path(template_value), 'packages.txt')
    if os.path.exists(packages_file):
        with open(packages_file, 'r') as f:
            return f.read().splitlines()
    return []


def handle_template_requirements(template_value: str):
    """
    Handle pip requirements for template
    """
    _check_pip_requirements(_get_template_required_packages(
        template_value), template_value)




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


def get_template_path(template_value: str) -> str:
    """
    Get path to template directory
    """
    template_dir = os.path.join('templates', template_value)
    return buildAppUtils.get_templates_data_path(os.path.normpath(template_dir))


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
        print(f'dashtools: init: Failed')
        exit(1)

    # Copy files from template directory
    template_base_path = get_template_path(template.value)
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

    # Handle pip requirements
    handle_template_requirements(template.value)
    print(
        f'dashtools: init: Created new app {app_name} at {os.path.join(target_dir, app_name)} with {template.name} template')


class TemplatePreviewResponse:
    object: Union[html.Div, None] = None
    needs_module: Union[str, None] = None

def try_get_template_preview(template_value:str) -> TemplatePreviewResponse:
    response = TemplatePreviewResponse()
    temp_path = get_template_path(Templates.Template(template_value).value)
    sys.path.append(temp_path)
    try:
        import preview
        sys.path.remove(temp_path)
        del sys.modules["preview"]
        response.object=preview.render()
    except ModuleNotFoundError as e:
        sys.path.remove(temp_path)
        missing_mod = e.msg.split("'")[1]
        response.needs_module=missing_mod.replace('_','-') if missing_mod != "preview" else None
    return response