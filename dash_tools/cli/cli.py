'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 12:47:58
 # Thanks to https://mike.depalatis.net/blog/simplifying-argparse.html
'''
import os
import argparse
from dash_tools.deploy import deployHeroku
from dash_tools.templating import buildApp, buildAppUtils, createTemplate
from dash_tools.runtime import runtimeUtils
from dash_tools.version import __version__


parser = argparse.ArgumentParser(
    description=f'The dash-tools v{__version__} CLI for Plotly Dash. See https://github.com/andrew-hossack/dash-tools for more information.')

subparsers = parser.add_subparsers(dest="subcommand")


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.
    """
    return (list(name_or_flags), kwargs)


def subcommand(args=[], parent=subparsers):
    """Decorator to define a new subcommand in a sanity-preserving way.
    The function will be stored in the ``func`` variable when the parser
    parses arguments so that it can be called directly like so::
        args = cli.parse_args()
        args.func(args)
    Usage example::
        @subcommand([argument("-d", help="Enable debug mode", action="store_true")])
        def subcommand(args):
            print(args)
    Then on the command line::
        $ python cli.py subcommand -d
    """
    def decorator(func):
        parser = parent.add_parser(func.__name__, description=func.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)
    return decorator


parser.add_argument(
    '-v',
    '--version',
    action='version',
    version=__version__)


@subcommand(
    [
        argument(
            "init",
            help='Create a new Dash app. Args: REQUIRED: <app name> OPTIONAL: <template> (Default: "default").',
            metavar='<app name> [<template>]',
            nargs='+'),
        argument(
            '--dir',
            '-d',
            help='Specify the directory to create the app in. Default: current directory.',
            default=os.getcwd(),
            metavar='<directory>',
            nargs='?')
    ])
def init(args):
    """Initialize a new app."""
    if args.dir is None:
        print('dash-tools: init: No directory specified')
        exit('dash-tools: init: Failed')
    buildApp.create_app(
        target_dir=args.dir,
        app_name=args.init[0],
        use_template=buildAppUtils.get_template_from_args(args))
    print(f'dash-tools: For an in-depth guide on configuring your app, see https://dash.plotly.com/layout')


@ subcommand(
    [
        argument(
            "--list",
            help="List available templates",
            default=False,
            action="store_true"),
        argument(
            "--init",
            help="Convert directory to a template. Args: REQUIRED: <directory to convert>",
            nargs=1),
    ])
def templates(args):
    if args.list:
        print('dash-tools: Templates usage example, type: dash-tools init MyApp csv')
        print('dash-tools: For more information on templates, see https://github.com/andrew-hossack/dash-tools#templates')
        print('dash-tools: templates: List of available templates:')
        buildAppUtils.print_templates()
    elif args.init:
        createTemplate.create_template(src=args.init[0], dest=os.getcwd())
    else:
        print('dash-tools: templates error: too few arguments')
        exit('dash-tools: Available templates options: --list, --init')


@subcommand(
    [
        argument(
            "--deploy",
            help="Deploys the current project <app name> to Heroku. Run command from the root of the project. --deploy takes one or no argument: <app name> (e.g. dash-tools --deploy my-app) OR (dash-tools --deploy-heroku)",
            default=False,
            action="store_true",
        ),
        argument(
            "--update",
            help="Updates the current project <app name> to Heroku. Run command from the root of the project",
            default=False,
            action="store_true"),
    ])
def heroku(args):
    if args.deploy:
        deployHeroku.deploy_app_to_heroku(os.getcwd())
    elif args.update:
        raise NotImplementedError('TODO implement update functionality')
    else:
        print('dash-tools: heroku error: too few arguments')
        exit('dash-tools: Available heroku options: --deploy, --update')


@subcommand(
    [
        argument(
            "run",
            help="Run the app locally. Uses Procfile if available, else recursive search for app.py",
            default=False,
            action="store_true"),
    ])
def run(args):
    if args.run:
        try:
            runtimeUtils.run_app(os.getcwd())
        except RuntimeError as e:
            print(e)
            exit('dash-tools: run: Failed')


def main():
    """
    dash-tools CLI entry point.
    """
    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
        exit('\ndash-tools: error: too few arguments')
    else:
        args.func(args)
