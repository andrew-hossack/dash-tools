import os

from dash import Dash, Input, Output, State, html, no_update, ctx
import dash_mantine_components as dmc
try:
    import alerts
    import tree
    from pages import deployPage
except ModuleNotFoundError:
    from . import tree
    from . import alerts
    from .pages import deployPage

from dash_iconify import DashIconify
from dashtools.deploy import fileUtils, herokuUtils


def generate_callbacks(app: Dash):

    @app.callback(
        Output('hidden-div', 'children'),
        Input('app-control-run-button', 'n_clicks'),
        Input('app-control-deploy-button', 'n_clicks'),
    )
    def run_deploy_buttons(run, deploy):
        button_clicked = ctx.triggered_id
        if button_clicked == 'app-control-run-button' and run:
            deployPage.terminal.writeln('Run Button Clicked')
        if button_clicked == 'app-control-deploy-button' and deploy:
            deployPage.terminal.writeln('Deploy Button Clicked')
        return html.Div()

    @app.callback(
        Output('app-control-name-input', 'value'),
        Input('app-control-name-refresh', 'n_clicks')
    )
    def generate_name(n):
        if n:
            return herokuUtils.generate_valid_name()

    @app.callback(
        [
            Output('app-control-name-status', 'children'),
        ],
        Input('app-control-name-input', 'value')
    )
    def validate_app_name(app_name):
        if not app_name:
            return [
                dmc.Tooltip(
                    label="Enter an app name you would like to use.",
                    placement="center",
                    withArrow=True,
                    wrapLines=True,
                    width=220,
                    children=[
                        DashIconify(icon='bi:three-dots',
                                    width=40, color='gray')
                    ])]
        if not herokuUtils.validate_heroku_app_name(app_name):
            return [
                dmc.Tooltip(
                    label="Heroku app names must start with a letter, end with a letter or digit, can only contain lowercase letters, numbers, and dashes, and have a minimum length of 3 characters. Maximum 30 characters.",
                    placement="center",
                    withArrow=True,
                    wrapLines=True,
                    width=220,
                    children=[
                        DashIconify(icon='bi:x-circle', width=40, color='red')
                    ])
            ]
        if not herokuUtils.check_heroku_app_name_available(app_name):
            return [
                dmc.Tooltip(
                    label=f"App name {app_name} is already taken on Heroku! Please choose a unique name.",
                    placement="center",
                    withArrow=True,
                    wrapLines=True,
                    width=220,
                    children=[
                        DashIconify(icon='bi:x-circle', width=40, color='red')
                    ])
            ]
        return [
            dmc.Tooltip(
                label=f"App name is available on Heroku",
                placement="center",
                withArrow=True,
                wrapLines=True,
                children=[
                    DashIconify(icon='bi:check-circle',
                                width=40, color='green')
                ])
        ]

    @ app.callback(
        [
            Output('deploy-terminal', 'value'),
            Output('deploy-terminal-runjs', 'run'),
        ],
        Input('deploy-terminal-refresh-interval', 'n_intervals'),
        State('deploy-terminal', 'value'),

    )
    def update_terminal(n, current_value):
        logCMD = '''
             var textarea = document.getElementById('deploy-terminal');
             textarea.scrollTop = textarea.scrollHeight;
             '''
        new_value = deployPage.terminal.read()
        if current_value != new_value:
            return new_value, logCMD
        return no_update, ""

    @ app.callback(
        [
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
                # TODO Check if isValidDashApp - might need to make helper function
                return (
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

    @ app.callback([
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
                    return (
                        '\n'.join(children),
                        True,
                        filepath,
                        html.Div(),
                    )
                except PermissionError as e:
                    # TODO write to error modal
                    return '\n'.join(children), True, '', alerts.render(key='PermissionError')
                    # children = [str(x) for x in list(pathlib.Path(".").rglob("*"))]
                    # TODO implement something like this
                    # https://www.cssscript.com/folder-tree-json/
        return '\n'.join(children), True, '', alerts.render(key='FileNotFoundError')
