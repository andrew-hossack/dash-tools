import os

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, ctx, html, no_update

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
                f'{runtimeUtils._python_shell_cmd()} {os.path.join(deployPage.fileExplorerInstance.root, "src/app.py")}')
            # deployPage.terminal.command('python3 --help')
        if button_clicked == 'app-control-deploy-button' and deploy:
            deployPage.terminal.writeln(
                f'Deploy Button Clicked TODO {deployPage.fileExplorerInstance.appName} at {deployPage.fileExplorerInstance.root}')
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
    def save_app_name(app_name):
        deployPage.fileExplorerInstance.appName = app_name

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
        Output('file-explorer-refresh-interval', 'disabled'),
        Output('readiness-check-trigger', 'children'),
        Input('file-explorer-button', 'n_clicks',),
        State('file-explorer-input', 'value'),
        prevent_initial_call=True
    )
    def toggle_readiness_check_refresh_interval(n, filepath):
        ENABLED = False
        if (filepath and n) and os.path.isdir(filepath):
            return ENABLED, no_update
        return not ENABLED, 'update doesnt matter'

    @ app.callback(
        Output('readiness-check-app-exists', 'children'),
        Output('readiness-check-render-yaml-exists', 'children'),
        Output('readiness-check-requirements-exists', 'children'),
        Output('readiness-check-hook-exists', 'children'),
        Output('readiness-check-render-yaml-generator-vis',
               component_property='style'),
        Output('readiness-check-requirements-generator-vis',
               component_property='style'),
        Input('file-explorer-refresh-interval', 'n_intervals'),
        Input('readiness-check-trigger', 'children')
    )
    def readiness_check(interval, change):
        DISPLAY_ON = {'display': 'inline-block'}
        DISPLAY_OFF = {'display': 'none'}
        filepath = deployPage.fileExplorerInstance.root
        if filepath:
            app_exists = fileUtils.check_file_exists(
                filepath, os.path.join('src', 'app.py'))
            render_yaml_exists = fileUtils.check_file_exists(
                filepath, 'render.yaml')
            requirements_exists = fileUtils.check_file_exists(
                filepath, 'requirements.txt')
            hook_exists = fileUtils.search_appfile_ui(
                filepath)
            deployPage.fileExplorerInstance.renderYamlExists = render_yaml_exists
            deployPage.fileExplorerInstance.requirementsExists = requirements_exists
            deployPage.fileExplorerInstance.serverHookExists = hook_exists
            return (
                deployPage.ReadinessStatus('PASS').get(
                ) if app_exists else deployPage.ReadinessStatus('FAIL').get(),
                deployPage.ReadinessStatus('PASS').get(
                ) if render_yaml_exists else deployPage.ReadinessStatus('FAIL').get(),
                deployPage.ReadinessStatus('PASS').get(
                ) if requirements_exists else deployPage.ReadinessStatus('FAIL').get(),
                deployPage.ReadinessStatus('PASS').get(
                ) if hook_exists else deployPage.ReadinessStatus('FAIL').get(),
                DISPLAY_ON if not render_yaml_exists else DISPLAY_OFF,
                DISPLAY_ON if not requirements_exists else DISPLAY_OFF
            )
        else:
            deployPage.fileExplorerInstance.renderYamlExists = False
            deployPage.fileExplorerInstance.requirementsExists = False
            deployPage.fileExplorerInstance.serverHookExists = False
            return (deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), DISPLAY_OFF, DISPLAY_OFF)

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
                    deployPage.fileExplorerInstance.root = filepath
                    deployPage.terminal.writeln(
                        'TODO update file tree when Deployment Readiness changes')
                    return (
                        html.Div(tree.FileTree(filepath).render(),
                                 style={'height': '100%', 'overflow': 'scroll'}),
                        True,
                        None,
                        html.Div()
                    )
                except PermissionError:
                    deployPage.fileExplorerInstance.root = None
                    return [], True, 'Permission Error', alerts.render(key='PermissionError')
        deployPage.fileExplorerInstance.root = None
        return [], True, 'File Not Found', alerts.render(key='FileNotFoundError')

    @ app.callback(
        Output('hidden-div', 'style'),
        Input('readiness-check-render-yaml-generator-button', 'n_clicks'),
        Input('readiness-check-requirements-generator-button', 'n_clicks'),
        prevent_initial_callback=True
    )
    def run_file_gen_function(n_1, n_2):
        button_id = ctx.triggered_id
        filepath = deployPage.fileExplorerInstance.root
        if filepath is not None:
            if button_id == 'readiness-check-render-yaml-generator-button':
                deployPage.terminal.writeln('$ Generating render.yaml ...')
                # TODO need to HAVE an app name before doing this
                # TODO also need to VALIDATE app name; update heroku name check
                fileUtils.create_render_yaml(
                    filepath, deployPage.fileExplorerInstance.appName)
                deployPage.terminal.writeln(
                    f'$ render.yaml successfully generated in {filepath}')

            elif button_id == 'readiness-check-requirements-generator-button':
                deployPage.terminal.writeln(
                    '$ Generating requirements.txt ...')
                fileUtils.create_requirements_txt(filepath)
                deployPage.terminal.writeln(
                    f'$ requirements.txt successfully generated in {filepath}')
