'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 13:57:48
 # Build dash apps with dash-tools
'''

import os

from .fileUtils import _get_data_path, _format_file_stream, _make_base_src_dir


def create_file_from_template(template_file: str, route: os.PathLike, app_name: str):
    """
    Save a file from a template to the given route.
    Example:
        create_file_from_template('home.py.template', './app_name/containers/home.py', app_name)
        >> Saves to ./app_name/containers/home.py
    """
    with open(route, 'w') as f:
        with open(_get_data_path(os.path.join('templates', template_file)), 'r') as t:
            f.write(_format_file_stream(t, app_name))


def create_app(base_dir: os.PathLike, app_name: str):
    '''
    Create a new app in the target directory.
    '''

    BASE_DIR, APP_SRC_DIR = _make_base_src_dir(base_dir, app_name)

    ##### Top-Level Base Files ./AppName/ #####
    ################################################################################

    # ./AppName/README.md
    create_file_from_template(
        'README.md.template',
        os.path.join(BASE_DIR, 'README.md'),
        app_name)

    ##### App src Files ./AppName/AppName/__init__.py #####
    ################################################################################

    create_file_from_template(
        '__init__.py.template',
        os.path.join(APP_SRC_DIR, '__init__.py'),
        app_name)

    # ./AppName/AppName/app.py
    create_file_from_template(
        'app.py.template',
        os.path.join(APP_SRC_DIR, 'app.py'),
        app_name)

    ##### Components ./AppName/AppName/components #####
    ################################################################################

    os.makedirs(os.path.join(APP_SRC_DIR, 'components'))

    # ./AppName/AppName/components/__init__.py
    create_file_from_template(
        '__init__.py.template',
        os.path.join(APP_SRC_DIR, 'components', '__init__.py'),
        app_name)

    # ./AppName/AppName/components/header.py
    create_file_from_template(
        'navbar.py.template',
        os.path.join(APP_SRC_DIR, 'components', 'header.py'),
        app_name)

    # ./AppName/AppName/components/footer.py
    create_file_from_template(
        'footer.py.template',
        os.path.join(APP_SRC_DIR, 'components', 'footer.py'),
        app_name)

    ##### Containers ./AppName/AppName/containers #####
    ################################################################################

    os.makedirs(os.path.join(APP_SRC_DIR, 'containers'))

    # ./AppName/AppName/containers/__init__.py
    create_file_from_template(
        '__init__.py.template',
        os.path.join(APP_SRC_DIR, 'containers', '__init__.py'),
        app_name)

    # ./AppName/AppName/containers/home.py
    create_file_from_template(
        'home.py.template',
        os.path.join(APP_SRC_DIR, 'containers', 'home.py'),
        app_name)
