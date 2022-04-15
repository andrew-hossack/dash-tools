'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 12:47:58
'''
import os
import argparse
from dash_tools.deploy import deployHeroku
from dash_tools.templating import buildTemplate, templateUtils
from dash_tools.version import __version__


def main():
    """
    dash-tools CLI entry point.
    """

    parser = argparse.ArgumentParser(
        description='The dash-tools CLI for Plotly Dash.')

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=__version__)

    parser.add_argument(
        '-i',
        '--init',
        help='Create a new Dash app. Args: REQUIRED: <app name> OPTIONAL: <template> (Default: "default").',
        nargs='+')

    parser.add_argument(
        '-t',
        '--templates',
        help='List available templates.',
        default=False,
        action='store_true')

    parser.add_argument(
        '--deploy-heroku',
        help='Deploys the current project <app name> to Heroku. Run command from the root of the project. Requires Heroku CLI and Git CLI. Args: REQUIRED: <app name>',
        nargs=1)

    handle_args(parser)


def handle_args(parser: argparse.ArgumentParser):
    """
    Handles the arguments passed to the CLI.
    """
    args = parser.parse_args()

    # Check that there is at least one argument passed to the CLI
    if (not args.init and not args.templates and not args.deploy_heroku):
        parser.print_help()
        exit('\ndash-tools: error: too few arguments')

    if args.init:
        buildTemplate.create_app(
            base_dir=os.getcwd(),
            app_name=args.init[0],
            use_template=templateUtils.get_template_from_args(args))
        print(f'dash-tools: For a step-by-step guide on configuring your app, see https://github.com/andrew-hossack/dash-tools/blob/main/README.md#usage-examples')

    if args.templates:
        print('dash-tools: templates: List of available templates:')
        templateUtils.print_templates()

    if args.deploy_heroku:
        deployHeroku.deploy_app_to_heroku(os.getcwd(), args.deploy_heroku[0])
