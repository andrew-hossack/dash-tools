'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 12:47:58
'''
import os
import argparse
from dash_tools.templating import buildTemplate
from dash_tools.templating import templateUtils
from dash_tools.meta import metaDataUtils


def main(parser: argparse.ArgumentParser = None, invoke_directory: os.PathLike = None):
    """
    dash-tools CLI entry point.

    Args:
        parser: The parser to use.
        invoke_directory: The directory command was invoked from.
    """
    args = parser.parse_args()

    if not (args.init or args.templates):
        parser.print_help()
        exit('\ndash-tools: error: too few arguments')

    if args.init:

        possible_template = args.init[1] if len(
            args.init) > 1 else templateUtils.Templates.DEFAULT

        print('dash-tools: init')

        buildTemplate.create_app(
            base_dir=invoke_directory,
            app_name=args.init[0],
            use_template=possible_template)

        metaDataUtils.add_project_metadata(
            invoke_directory,
            args.init[0],
            possible_template)

        print(
            f'dash-tools: init: finished')

    if args.templates:
        print('dash-tools: templates: List of available templates:')

        for template in templateUtils.Templates:
            print(f'{template.value}')
