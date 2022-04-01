'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-01 13:57:48
 # Build dash apps with dash-tools
'''

import os

from .fileUtils import _get_data_path, format_file_stream, _make_base_src_dir


def move_and_format_template_file(templates_src: os.PathLike, dest: os.PathLike, app_name: str):
    """
    Save a templates_src file to a dest file location.

    :param templates_src: The template file to copy
    :param dest: The destination file to save to
    :param app_name: The name of the app

    Example:
        move_and_format_template_file(
            'home.py.template', './app_name/containers/home.py', app_name)
        >>> Looks for /templates/home.py.template and saves to ./app_name/containers/home.py
    """
    with open(dest, 'w') as f:
        with open(_get_data_path(os.path.join('templates', templates_src)), 'r') as t:
            # Format file, replacing artifacts like {app_name} or {createTime}
            formatted_file = format_file_stream(t, app_name)
            f.write(formatted_file)


def move_template_file_bytes(templates_src: os.PathLike, dest: os.PathLike):
    """
    Save a templates_src file to a dest file location. Performs a file copy instead.

    Useful for files that are not text files.
    """
    with open(dest, 'wb') as f:
        with open(_get_data_path(os.path.join('templates', templates_src)), 'rb') as t:
            f.write(t.read())


def create_app(base_dir: os.PathLike, app_name: str):
    '''
    Create a new app in the target directory.

    Looks for files in the /template directory
    '''

    BASE_DIR, APP_SRC_DIR = _make_base_src_dir(base_dir, app_name)

    ##### Top-Level Base Files ./AppName/ #####
    ################################################################################

    # ./AppName/README.md
    move_and_format_template_file(
        'README.md.template',
        os.path.join(BASE_DIR, 'README.md'),
        app_name)

    ##### App src Files ./AppName/AppName/__init__.py #####
    ################################################################################

    move_and_format_template_file(
        '__init__.py.template',
        os.path.join(APP_SRC_DIR, '__init__.py'),
        app_name)

    # ./AppName/AppName/app.py
    move_and_format_template_file(
        'app.py.template',
        os.path.join(APP_SRC_DIR, 'app.py'),
        app_name)

    ##### Components ./AppName/AppName/components #####
    ################################################################################

    os.makedirs(os.path.join(APP_SRC_DIR, 'components'))

    # ./AppName/AppName/components/__init__.py
    move_and_format_template_file(
        '__init__.py.template',
        os.path.join(APP_SRC_DIR, 'components', '__init__.py'),
        app_name)

    # ./AppName/AppName/components/header.py
    move_and_format_template_file(
        'navbar.py.template',
        os.path.join(APP_SRC_DIR, 'components', 'header.py'),
        app_name)

    # ./AppName/AppName/components/footer.py
    move_and_format_template_file(
        'footer.py.template',
        os.path.join(APP_SRC_DIR, 'components', 'footer.py'),
        app_name)

    ##### Containers ./AppName/AppName/containers #####
    ################################################################################

    os.makedirs(os.path.join(APP_SRC_DIR, 'containers'))

    # ./AppName/AppName/containers/__init__.py
    move_and_format_template_file(
        '__init__.py.template',
        os.path.join(APP_SRC_DIR, 'containers', '__init__.py'),
        app_name)

    # ./AppName/AppName/containers/home.py
    move_and_format_template_file(
        'home.py.template',
        os.path.join(APP_SRC_DIR, 'containers', 'home.py'),
        app_name)

    ##### Assets ./AppName/AppName/assets #####
    ################################################################################

    os.makedirs(os.path.join(APP_SRC_DIR, 'assets'))

    # ./AppName/AppName/assets/style.css
    move_and_format_template_file(
        os.path.join('assets', 'style.css.template'),
        os.path.join(APP_SRC_DIR, 'assets', 'style.css'),
        app_name)

    # ./AppName/AppName/assets/loading.css
    move_and_format_template_file(
        os.path.join('assets', 'loading.css.template'),
        os.path.join(APP_SRC_DIR, 'assets', 'loading.css'),
        app_name)

    # ./AppName/AppName/assets/favicon.ico
    move_template_file_bytes(
        os.path.join('assets', 'favicon.ico.template'),
        os.path.join(APP_SRC_DIR, 'assets', 'favicon.ico'))

    ##### Assets ./AppName/AppName/assets/img #####
    ################################################################################

    os.makedirs(os.path.join(APP_SRC_DIR, 'assets', 'img'))

    # ./AppName/AppName/assets/loader.gif
    move_template_file_bytes(
        os.path.join('assets', 'loader.gif.template'),
        os.path.join(APP_SRC_DIR, 'assets', 'img', 'loader.gif'))
