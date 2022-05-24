'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 12:47:58
 # Thanks to https://mike.depalatis.net/blog/simplifying-argparse.html
'''
import argparse
import os
import sys as _sys
from dashtools.deploy import deployHeroku
from dashtools.runtime import runtimeUtils
from dashtools.templating import buildApp, buildAppUtils, createTemplate
from dashtools.version import __version__


class MyArgumentParser(argparse.ArgumentParser):
    """Override default help message"""

    def print_help(self, file=None):
        if file is None:
            file = _sys.stdout
        message = f"""The dashtools v{__version__} CLI for Plotly Dash. See https://github.com/andrew-hossack/dash-tools for more details.
\nUsage:
    {'dashtools <command> [options]':<29}
\nCommands and Options:
    {'heroku':<29}Handle Heroku deployment. Choose option:
        {'--deploy':<25}Deploys the current project to Heroku
        {'--update [remote name]':<25}Push changes to existing Heroku remote
    
    {'init <app name> [template]':<29}Create a new app
        {'--dir, -d':<25}Specify alternative create location
    
    {'run':<29}Run app locally from the current directory
    
    {'templates':<29}List and create templates
        {'--init <directory>':<25}Creates a template from specified directory
        {'--list':<25}List available templates
\nOther Options:
    {'--help, -h':<29}Display help message
    {'--version, -v':<29}Display version
"""
        file.write(message+"\n")


parser = MyArgumentParser()

parser._positionals.title = 'Positional Arguments'
parser._optionals.title = 'Optional Arguments'

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
    version=f'dashtools {__version__}')


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
            help='Specify the directory to create the app in. Args: REQUIRED: <directory>',
            default=os.getcwd(),
            metavar='<directory>',
            nargs='?')
    ])
def init(args):
    """Initialize a new app."""
    if args.dir is None:
        print('dashtools: init: No directory specified. Usage Example: dashtools init MyDashApp -d ~/Desktop')
        exit('dashtools: init: Failed')
    buildApp.create_app(
        target_dir=args.dir,
        app_name=args.init[0],
        template=buildAppUtils.get_template_from_args(args))
    print(
        f'dashtools: Run your app using the "cd {args.init[0]} && dashtools run" command')
    print(f'dashtools: For an in-depth guide on configuring your app, see https://dash.plotly.com/layout')


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
        print('dashtools: Templates usage example, type: dashtools init MyApp csv')
        print('dashtools: templates: List of available templates:')
        buildAppUtils.print_templates()
    elif args.init:
        createTemplate.create_template(src=args.init[0], dest=os.getcwd())
    else:
        print('dashtools: templates error: too few arguments')
        print('dashtools: For more information on templates, see https://github.com/andrew-hossack/dash-tools#templates')
        exit('dashtools: Available templates options: --list, --init')


@subcommand(
    [
        argument(
            "--deploy",
            help="Deploys the current project to Heroku. Run command from the root of the project",
            default=False,
            action="store_true",
        ),
        argument(
            "--update",
            help="Updates the current project to Heroku. Run command from the root of the project. Args: OPTIONAL: <git remote>",
            nargs="?",
            const="heroku",
            type=str
        ),
    ])
def heroku(args):
    if args.deploy:
        deployHeroku.deploy_app_to_heroku(os.getcwd())
    elif args.update:
        deployHeroku.update_heroku_app(args.update)
    else:
        print('dashtools: heroku error: too few arguments')
        exit('dashtools: Available heroku options: --deploy, --update')


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
            exit('dashtools: run: Failed')


def main():
    """
    dashtools CLI entry point.
    """
    args = parser.parse_args()
    if args.subcommand is None:
        parser.print_help()
    else:
        args.func(args)
