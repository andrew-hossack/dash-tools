import os
from dash import Dash, Input, Output, State, html, no_update, ctx, dcc
import dash_mantine_components as dmc

from dashtools.dashboard.pages.deployPage import ReadinessStatus
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
from dashtools.runtime import runtimeUtils


def generate_callbacks(app: Dash):

    @app.callback(
        Output('hidden-div', 'children'),
        Input('app-control-run-button', 'n_clicks'),
        Input('app-control-deploy-button', 'n_clicks'),
        Input('deploy-terminal-clear-button', 'n_clicks')
    )
    def run_deploy_buttons(run, deploy, clear_terminal):
        button_clicked = ctx.triggered_id
        if button_clicked == 'app-control-run-button' and run:
            # TODO if no runtime command is found then gracefully fail
            # TODO capture stdout
            # TODO review if this will actually work
            deployPage.terminal.command(
                f'{runtimeUtils._python_shell_cmd()} {os.path.join(deployPage.herokuApplication.root, "src/app.py")}')
            # deployPage.terminal.command('python3 --help')
        if button_clicked == 'app-control-deploy-button' and deploy:
            deployPage.terminal.writeln(
                f'Deploy Button Clicked TODO {deployPage.herokuApplication.appName} at {deployPage.herokuApplication.root}')
        if button_clicked == 'deploy-terminal-clear-button' and clear_terminal:
            deployPage.terminal.clear()
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
            deployPage.herokuApplication.appName = None
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
            deployPage.herokuApplication.appName = None
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
            deployPage.herokuApplication.appName = None
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
        deployPage.herokuApplication.appName = app_name
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
        Output('readiness-check-hook-exists', 'children'),
        Output('readiness-check-runtime-exists', 'children'),
        Output('readiness-check-requirements-exists', 'children'),
        Output('readiness-check-procfile-exists', 'children'),
        Output('readiness-check-app-exists', 'children'),
        Input('file-explorer-button', 'n_clicks'),
        State('file-explorer-input', 'value')
    )
    def readiness_check_callback(n, filepath):
        if (filepath and n):
            if os.path.isdir(filepath):
                return (
                    deployPage.ReadinessStatus('PASS').get() if fileUtils.verify_procfile(
                        filepath)['valid'] else deployPage.ReadinessStatus('FAIL').get(),
                    deployPage.ReadinessStatus('PASS').get() if fileUtils.check_file_exists(
                        filepath, 'runtime.txt') else deployPage.ReadinessStatus('FAIL').get(),
                    deployPage.ReadinessStatus('PASS').get() if fileUtils.check_file_exists(
                        filepath, 'requirements.txt') else deployPage.ReadinessStatus('FAIL').get(),
                    deployPage.ReadinessStatus('PASS').get() if fileUtils.check_file_exists(
                        filepath, 'Procfile') else deployPage.ReadinessStatus('FAIL').get(),
                    deployPage.ReadinessStatus('PASS').get() if fileUtils.check_file_exists(
                        filepath, os.path.join('src', 'app.py')) else deployPage.ReadinessStatus('FAIL').get()
                )
        return (deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get())

    @ app.callback(
        [
            Output('file-explorer-output', 'children'),
            Output('file-explorer-input', 'required'),
            Output('file-explorer-input', 'error'),
            Output('notifications-container', 'children'),
        ],
        Input('file-explorer-button', 'n_clicks'),
        State('file-explorer-input', 'value')
    )
    def file_explorer_callback(n, filepath: os.PathLike):
        # Initial callbacks
        if not n:
            return html.Div(), False, None, html.Div()
        if filepath:
            if os.path.isdir(filepath):
                try:
                    deployPage.herokuApplication.root = filepath
                    return (
                        html.Div(tree.FileTree(filepath).render(),
                                 style={'height': '100%', 'overflow': 'scroll'}),
                        True,
                        None,
                        html.Div(),
                    )
                except PermissionError:
                    deployPage.herokuApplication.root = None
                    return [], True, 'Permission Error', alerts.render(key='PermissionError')
        deployPage.herokuApplication.root = None
        return [], True, 'File Not Found', alerts.render(key='FileNotFoundError')
