'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 12:47:58
'''
import os
import argparse
from dash_tools.templating import buildTemplate
from dash_tools.templating.templateUtils import Templates


def main(parser: argparse.ArgumentParser = None, invoke_directory: os.PathLike = None):
    """
    dash-tools CLI entry point.

    Args:
        parser: The parser to use.
        invoke_directory: The directory command was invoked from.
    """
    args = parser.parse_args()

    if not (args.init or args.run or args.dev or args.use_stack):
        parser.print_help()
        exit('\ndash-tools: error: too few arguments')

    if args.init:
        possible_template = args.init[1] if len(
            args.init) > 1 else Templates.DEFAULT
        print('dash-tools: init')
        buildTemplate.create_app(
            base_dir=invoke_directory,
            app_name=args.init[0],
            use_template=possible_template)
        print(
            f'dash-tools: init: finished creating new app {args.init[0]} at {invoke_directory}')

    if args.run:
        print(f'dash-tools: run: running app in normal mode')

    if args.dev:
        print(f'dash-tools: run: running app in dev mode')

    if args.use_stack:
        print(
            f'dash-tools: use-stack: adding stack framework {args.use_stack[0]}')
