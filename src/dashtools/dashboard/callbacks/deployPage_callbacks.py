import os
import time

import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, ctx, dcc, html, no_update

try:
    import alerts
    import tree
    from dashtools.dashboard.pages import deployPage
    from dashtools.deploy import fileUtils, gitUtils, herokuUtils
except ModuleNotFoundError:
    from .. import tree
    from .. import alerts
    from ..pages import deployPage
    from ...deploy import fileUtils, gitUtils, herokuUtils

from dash_iconify import DashIconify


def generate_callbacks(app: Dash):

    @app.callback(
        Output('hidden-div', 'children'),
        Input('app-control-deploy-button', 'n_clicks'),
        Input('deploy-terminal-clear-button', 'n_clicks')
    )
    def deploy_button(deploy, clear_terminal):
        button_clicked = ctx.triggered_id
        if button_clicked == 'app-control-deploy-button' and deploy:
            fileUtils.set_render_yaml_service_name(
                os.path.join(deployPage.fileExplorerInstance.root, 'render.yaml'), deployPage.fileExplorerInstance.appName)
            gitUtils.commit_and_push(
                cwd=deployPage.fileExplorerInstance.root, commit_message=f'DashTools Automatic Push - {time.strftime("%m/%d/%Y @ %H:%M:%S")}')
            deployPage.terminal.writeln(
                '$ Follow instructions on Render.com to finish deployment')
        if button_clicked == 'deploy-terminal-clear-button' and clear_terminal:
            deployPage.terminal.clear()
        return html.Div()

    @app.callback(
        Output('app-control-name-input', 'value'),
        Input('app-control-name-refresh', 'n_clicks'),
        Input('file-explorer-button', 'n_clicks'),
    )
    def app_control_name_input(gen_button, file_explorer_button):
        callback_ctx = ctx.triggered_id
        if gen_button and callback_ctx == 'app-control-name-refresh':
            return herokuUtils.generate_valid_name()
        if file_explorer_button and callback_ctx == 'file-explorer-button':
            # update current value to render.yaml value
            # time.sleep is not ideal, but we need to wait for other
            # values to populate first
            time.sleep(2)
            if deployPage.fileExplorerInstance.renderYamlExists:
                render_yaml_path = os.path.join(
                    deployPage.fileExplorerInstance.root, 'render.yaml')
                return fileUtils.get_render_yaml_service_name(render_yaml_path)

    @app.callback(
        Output('app-control-name-status', 'children'),
        Input('app-control-name-input', 'value')
    )
    def save_app_name(app_name):
        if app_name:
            deployPage.fileExplorerInstance.appName = app_name
            return [dmc.Tooltip(
                label=f"Looks great! Render may change this name if it is not unique.",
                withArrow=True,
                multiline=True,
                width=220,
                children=[
                    DashIconify(icon='bi:check-circle',
                                width=30, color='green')
                ])]
        else:
            deployPage.fileExplorerInstance.appName = None
            return [dmc.Tooltip(
                label="Enter an app name you would like to use. Render may change this name if it is not unique.",
                withArrow=True,
                multiline=True,
                width=220,
                children=[
                    DashIconify(icon='bi:three-dots',
                                width=30, color='gray')
                ])]

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
        Input('file-explorer-button', 'n_clicks'),
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
        Output('readiness-check-on-github', 'children'),
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
            deployPage.fileExplorerInstance.setGithubUrl(
                gitUtils.get_remote_url(cwd=filepath))
            githubUrlExists = deployPage.fileExplorerInstance.githubUrl
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
                deployPage.ReadinessStatus('PASS').get(
                ) if githubUrlExists else deployPage.ReadinessStatus('FAIL').get(),
                DISPLAY_ON if not render_yaml_exists else DISPLAY_OFF,
                DISPLAY_ON if not requirements_exists else DISPLAY_OFF
            )
        else:
            deployPage.fileExplorerInstance.renderYamlExists = False
            deployPage.fileExplorerInstance.requirementsExists = False
            deployPage.fileExplorerInstance.serverHookExists = False
            return (deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), deployPage.ReadinessStatus('PENDING').get(), DISPLAY_OFF, DISPLAY_OFF)

    @ app.callback(
        [
            Output('file-explorer-output', 'children'),
            Output('file-explorer-input', 'required'),
            Output('file-explorer-input', 'error'),
            Output('notifications-container-file-explorer', 'children'),
        ],
        Input('file-explorer-button', 'n_clicks'),
        Input('update-filetree-hidden', 'children'),
        State('file-explorer-input', 'value'),
        prevent_initial_callback=True
    )
    def file_explorer_callback(n, force_tree_update, filepath: os.PathLike):
        # Initial callbacks
        trigger_id = ctx.triggered_id
        empty_div = dmc.Center([
            html.H3("Open a File to Continue", style={
                    'opacity': '10%', 'padding-top': '50px'})
        ])
        if not n:
            return empty_div, False, None, html.Div()
        if filepath:
            filepath = os.path.normpath(filepath)
            if os.path.isdir(filepath):
                try:
                    deployPage.fileExplorerInstance.root = filepath
                    if trigger_id == "file-explorer-button":
                        deployPage.terminal.writeln(f'$ Selected file {filepath}')
                    alerts_list = []
                    if not gitUtils.git_is_installed():
                        deployPage.terminal.writeln(
                            "$ Error: Git must be installed on your machine before continuing! Check out https://git-scm.com/book/en/v2/Getting-Started-Installing-Git for more details.")
                        alerts_list.append(alerts.render(
                            key='GitNotInstalledError'))
                    return (
                        html.Div(
                            tree.FileTree(filepath).render(),
                            style={'height': '100%', 'overflow': 'scroll'}),
                        True,
                        None,
                        html.Div(alerts_list)
                    )
                except PermissionError:
                    deployPage.fileExplorerInstance.root = None
                    return empty_div, True, 'Permission Error', alerts.render(key='PermissionError')
        deployPage.fileExplorerInstance.root = None
        return empty_div, True, 'File Not Found', alerts.render(key='FileNotFoundError')

    @ app.callback(
        Output('notifications-container-file-generator', 'children'),
        Output('update-filetree-hidden', 'children'),
        Input('readiness-check-render-yaml-generator-button', 'n_clicks'),
        Input('readiness-check-requirements-generator-button', 'n_clicks'),
        State('app-control-name-input', 'value'),
        prevent_initial_callback=True
    )
    def run_file_gen_function(n_1, n_2, app_name):
        button_id = ctx.triggered_id
        filepath = deployPage.fileExplorerInstance.root
        if filepath is not None:
            if button_id == 'readiness-check-render-yaml-generator-button' and n_1:
                if not app_name:
                    return (alerts.render(key="NameRequiredError"), no_update)
                deployPage.terminal.writeln('$ Generating render.yaml ...')
                fileUtils.create_render_yaml(
                    filepath, deployPage.fileExplorerInstance.appName)
                deployPage.terminal.writeln(
                    f'$ render.yaml successfully generated in {filepath}')
                return (no_update, 'update doesnt matter')

            elif button_id == 'readiness-check-requirements-generator-button' and n_2:
                deployPage.terminal.writeln(
                    '$ Generating requirements.txt ...')
                fileUtils.create_requirements_txt(filepath)
                deployPage.terminal.writeln(
                    f'$ requirements.txt successfully generated in {filepath}')
                # return no_update, 'update doesnt matter'
                return (no_update, 'different update dont matter')
        return (no_update, no_update)

    @app.callback(
        Output('deployment-readiness-status-output', 'children'),
        Output('app-control-deploy-button-container', 'children'),
        Input('file-explorer-refresh-interval', 'n_intervals'),
        Input('readiness-check-trigger', 'children'),
        prevent_initial_call=True
    )
    def deployment_readiness(n_intervals, trigger):
        if deployPage.fileExplorerInstance.isDeployReady():
            if not deployPage.fileExplorerInstance.deployReadyFlagCallback:
                deployPage.terminal.writeln(
                    '$ Your application is ready to be deployed! Press the DEPLOY TO RENDER button and follow on-screen instructions to deploy your app.')
            deployPage.fileExplorerInstance.deployReadyFlagCallback = True
            return (
                deployPage.build_checkbox('PASS', '**Ready**',
                                          'Your application is ready to be deployed to Render.com!', 'pass-deploy-status-id', text_margin_l='5px', tooltip_pos='top'),
                dmc.Button(
                    'Deploy',
                    variant="gradient",
                    leftIcon=[
                        dcc.Link(
                            [
                                html.Img(
                                    src='https://render.com/images/deploy-to-render-button.svg', alt="Deploy to Render")
                            ],
                            target="_blank",
                            href=f"https://render.com/deploy?repo={deployPage.fileExplorerInstance.githubUrl}")
                    ],
                    disabled=False,
                    style={'width': '200px'},
                    id='app-control-deploy-button')
            )
        else:
            _, status = deployPage.fileExplorerInstance.isDeployReadyWithStatus()
            deployPage.fileExplorerInstance.deployReadyFlagCallback = False
            status_str = [key for key, val in status.items() if not val]
            return (
                deployPage.build_checkbox("FAIL", '**Not Ready**',
                                          f'Required Items: {", ".join(status_str)}', 'fail-deploy-status-id', text_margin_l='5px', tooltip_pos='top'),
                dmc.Button(
                    'Deploy',
                    variant="gradient",
                    leftIcon=[
                        html.Img(
                            src='https://render.com/images/deploy-to-render-button.svg', alt="Deploy to Render")
                    ],
                    disabled=True,
                    style={'width': '200px', 'opacity': '0.6'},
                    id='app-control-deploy-button')
            )
