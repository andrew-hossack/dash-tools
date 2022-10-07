import os
from dash import Dash, Input, Output, State, no_update, html
try:
    from pages import deployPage
    import tree
    import alerts
except ModuleNotFoundError:
    from . import tree
    from . import alerts
    from .pages import deployPage
from dashtools.deploy import herokuUtils, fileUtils


def generate_callbacks(app: Dash):

    @app.callback(
        [
            Output('deploy-terminal', 'value'),
            Output('deploy-terminal-runjs', 'run'),
        ],
        Input('deploy-terminal-refresh-interval', 'n_intervals'),
        State('deploy-terminal', 'value'),
    )
    def update_terminal_text(n, current_value):
        logCMD = '''
             var textarea = document.getElementById('deploy-terminal');
             textarea.scrollTop = textarea.scrollHeight;
             '''
        # deployPage.terminal.command('ls')
        new_value = deployPage.terminal.read()
        if current_value != new_value:
            return new_value, logCMD
        return no_update, ""

    @app.callback(
        [
            Output('readiness-check-name-available', 'checked'),
            Output('readiness-check-hook-exists', 'checked'),
            Output('readiness-check-runtime-exists', 'checked'),
            Output('readiness-check-requirements-exists', 'checked'),
            Output('readiness-check-procfile-exists', 'checked'),
            Output('readiness-check-app-exists', 'checked'),
        ],
        Input('file-explorer-button', 'n_clicks'),
        State('file-explorer-input', 'value')
    )
    def readiness_check_callback(n, filepath):
        if filepath and n:
            if os.path.isdir(filepath):
                return (
                    # TODO Also need to validate app name validate_heroku_app_name()
                    herokuUtils.check_heroku_app_name_available(
                        'foo-app'),
                    # TODO require 'app.py' filename?
                    # TODO break out verify procfile and verify server=app.server exists
                    fileUtils.verify_procfile(filepath)['valid'],
                    fileUtils.check_file_exists(
                        filepath, 'runtime.txt'),
                    fileUtils.check_file_exists(
                        filepath, 'requirements.txt'),
                    fileUtils.check_file_exists(
                        filepath, 'Procfile'),
                    True if fileUtils.app_root_path(
                        filepath) else False
                )
        return False, False, False, False, False, False

    @app.callback([
        Output('file-explorer-output', 'value'),
        Output('file-explorer-input', 'required'),
        Output('file-explorer-input', 'value'),
        Output('notifications-container', 'children'),
    ],
        Input('file-explorer-button', 'n_clicks'),
        State('file-explorer-input', 'value')
    )
    def file_explorer_callback(n, filepath: os.PathLike):
        if not n:
            # Initial callbacks
            return '', False, '', html.Div()
        children = []
        if filepath:
            if os.path.isdir(filepath):
                try:
                    children = tree.tree(filepath)
                    deployPage.terminal.command(f'ls {filepath}')
                    return (
                        '\n'.join(children),
                        True,
                        filepath,
                        html.Div(),
                    )
                except PermissionError as e:
                    # TODO write to error modal
                    deployPage.terminal.writeln(
                        f'$ {filepath}\n{e}')
                    # children = [str(x) for x in list(pathlib.Path(".").rglob("*"))]
                    # TODO implement something like this
                    # https://www.cssscript.com/folder-tree-json/
        deployPage.terminal.clear()
        return '\n'.join(children), True, '', alerts.render()
