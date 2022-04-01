'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 13:57:48
 # Build dash apps with dash-tools
'''

import datetime
import os
from typing import IO
from pkg_resources import resource_filename


def get_data_path(data_dir: os.PathLike) -> os.PathLike:
    return resource_filename(__name__, data_dir)


def format_file_stream(t: IO, app_name: str) -> str:
    """
    Format the template file with given variables.
    """
    w = t.read().replace(r'{appName}', app_name)
    w = w.replace(r'{createTime}', str(datetime.datetime.now()))
    return w


def create_app(base_dir: os.PathLike, app_name: str):
    '''
    Create a new app in the target directory.
    '''

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    app_dir = os.path.join(base_dir, app_name)
    if os.path.exists(app_dir):
        exit(f'dash-tools: init: App {app_dir} already exists! Aborting.')

    # Top-level file
    # ./AppName/
    os.makedirs(app_dir)

    # Create the app directory
    # ./AppName/AppName
    app_src_dir = os.path.join(app_dir, app_name)
    os.makedirs(app_src_dir)

    # Create required files in app_src_dir

    # ./AppName/AppName/__init__.py
    with open(os.path.join(app_src_dir, '__init__.py'), 'w') as f:
        f.write('# Placeholder for __init__.py')

    # Create README.md
    # ./AppName/README.md
    with open(os.path.join(app_dir, 'README.md'), 'w') as f:
        with open(get_data_path('/templates/README.md.template'), 'r') as t:
            f.write(format_file_stream(t, app_name))

    # ./AppName/AppName/app.py
    with open(os.path.join(app_src_dir, 'app.py'), 'w') as f:
        with open(get_data_path('/templates/app.py.template'), 'r') as t:
            f.write(format_file_stream(t, app_name))

    # ./AppName/AppName/components
    os.makedirs(os.path.join(app_src_dir, 'components'))

    # ./AppName/AppName/components/__init__.py
    with open(os.path.join(app_src_dir, 'components', '__init__.py'), 'w') as f:
        f.write('# Placeholder for __init__.py')

    # ./AppName/AppName/components/header.py
    with open(os.path.join(app_src_dir, 'components', 'header.py'), 'w') as f:
        with open(get_data_path('/templates/navbar.py.template'), 'r') as t:
            f.write(format_file_stream(t, app_name))

    # ./AppName/AppName/components/footer.py
    with open(os.path.join(app_src_dir, 'components', 'footer.py'), 'w') as f:
        with open(get_data_path('/templates/footer.py.template'), 'r') as t:
            f.write(format_file_stream(t, app_name))

    # ./AppName/AppName/containers
    os.makedirs(os.path.join(app_src_dir, 'containers'))

    # ./AppName/AppName/containers/__init__.py
    with open(os.path.join(app_src_dir, 'containers', '__init__.py'), 'w') as f:
        f.write('# Placeholder for __init__.py')

    # ./AppName/AppName/containers/home.py
    with open(os.path.join(app_src_dir, 'containers', 'home.py'), 'w') as f:
        with open(get_data_path('/templates/home.py.template'), 'r') as t:
            f.write(format_file_stream(t, app_name))
