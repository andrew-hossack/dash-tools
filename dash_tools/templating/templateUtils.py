'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 19:12:04
 '''
import argparse
from pkg_resources import resource_filename
import os
from dash_tools.templating.Templates import Template


def print_templates():
    """
    Print the available templates.
    """
    for template in Template:
        print(f'\t> {template.value}')


def check_create_app_args(base_dir, app_name):
    """
    Check the arguments passed to the init command.
    """
    app_dir = os.path.join(base_dir, app_name)
    if os.path.exists(app_dir):
        exit(f'dash-tools: init: App {app_dir} already exists. Aborting.')


def get_templates_data_path(data_dir: os.PathLike) -> os.PathLike:
    """
    Get the path to the data directory.
    """
    return resource_filename(__name__, data_dir)


def get_template_from_args(args: argparse.Namespace) -> Template:
    """
    Get the template to use based on the arguments passed to the CLI.

    If the user passed in a template, use that, otherwise use the `default`.
    """
    return args.init[1] if len(
        args.init) > 1 else Template.DEFAULT


def convert_to_template_or_error(value) -> Template:
    """
    Convert the string passed to the init command to a template.
    """
    try:
        return Template(value)
    except ValueError:
        print(f'dash-tools: init: Template "{value}" is not a valid template.')
        print('Valid templates are:')
        print_templates()
        exit(1)
