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
        help='Deploys the current project <app name> to Heroku. Run command from the root of the project. --deploy-heroku takes either 1 argument: <app name> (e.g. dash-tools --deploy-heroku my-app) or no arguments (e.g. dash-tools --deploy-heroku)',
        nargs='?',
        type=str,
        const="None",
        dest='deploy_heroku'
    )

    handle_args(parser)


def handle_args(parser: argparse.ArgumentParser):
    """
    Handles the arguments passed to the CLI.
    """
    args = parser.parse_args()

    if args.init:
        buildTemplate.create_app(
            base_dir=os.getcwd(),
            app_name=args.init[0],
            use_template=templateUtils.get_template_from_args(args))
        print(f'dash-tools: For a step-by-step guide on configuring your app, see https://github.com/andrew-hossack/dash-tools/blob/main/README.md#usage-examples')

    elif args.templates:
        print('dash-tools: templates: List of available templates:')
        templateUtils.print_templates()

    elif args.deploy_heroku:
        app_name = args.deploy_heroku
        if args.deploy_heroku == "None":
            app_name = None
        deployHeroku.deploy_app_to_heroku(os.getcwd(), app_name)

    else:
        parser.print_help()
        exit('\ndash-tools: error: too few arguments')
