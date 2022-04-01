'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 13:57:48
 # Build dash apps with dash-tools
'''

import os


def create_app(target_dir: os.PathLike, app_name: str):
    '''
    Create a new app in the target directory.
    '''
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    app_dir = os.path.join(target_dir, app_name)
    if os.path.exists(app_dir):
        exit(f'dash-tools: init: App {app_dir} already exists! Aborting.')

    os.makedirs(app_dir)
