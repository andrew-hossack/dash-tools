'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 22:22:56
 # Generate metedata files for the dash-tools CLI.
'''

import datetime
import os
import json
from dash_tools.templating import templateUtils


def add_project_metadata(base_dir: str, app_name: str, template: templateUtils.Templates):
    """
    Generate metedata files for the dash-tools CLI in project directory.

    Args:
        base_dir: The directory the app is being created in.
        app_name: The name of the app being created.
    """
    app_path = os.path.join(base_dir, app_name)
    with open(os.path.join(app_path, '.dash-tools'), 'w') as f:
        f.write(json.dumps({
            'app_name': app_name,
            'base_dir': app_path,
            'template': template.value,
            'create_time': str(datetime.datetime.now()),
            'last_update': str(datetime.datetime.now())
        }))


def load_project_metadata(base_dir: str, app_name: str):
    """
    Load metedata files for the dash-tools CLI in project directory.

    Args:
        base_dir: The directory the app is being created in.
        app_name: The name of the app being created.
    """
    app_path = os.path.join(base_dir, app_name)
    with open(os.path.join(app_path, '.dash-tools'), 'r') as f:
        return json.loads(f.read())
