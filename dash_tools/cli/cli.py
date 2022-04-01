'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 12:47:58
'''
import os
import argparse
from dash_tools.templating import build_template


def main(parser: argparse.ArgumentParser = None, cwd: os.PathLike = None):
    args = parser.parse_args()

    if not (args.init or args.run or args.dev or args.use_stack):
        parser.print_help()
        exit('\ndash-tools: error: too few arguments')

    if args.init:
        print(f'dash-tools: init: creating new app {args.init[0]} at {cwd}')
        build_template.create_app(base_dir=cwd, app_name=args.init[0])

    if args.run:
        print(f'dash-tools: run: running app in normal mode')

    if args.dev:
        print(f'dash-tools: run: running app in dev mode')

    if args.use_stack:
        print(
            f'dash-tools: use-stack: adding stack framework {args.use_stack[0]}')
