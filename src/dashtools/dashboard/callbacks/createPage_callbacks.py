'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-10-23 14:52:57
'''


import os
import pathlib
from dash_iconify import DashIconify
from dash import Dash, Input, Output, State, no_update, ctx, html, ClientsideFunction
import dash_mantine_components as dmc
try:
    from dashtools.dashboard.pages import createPage
    from dashtools.dashboard import alerts
    from dashtools.templating import buildApp
except ModuleNotFoundError:
    from ..pages import createPage
    from .. import alerts
import threading


def generate_callbacks(app: Dash):
    @ app.callback(
        [
            Output('create-terminal', 'value'),
            Output('create-terminal-runjs', 'run'),
        ],
        Input('create-terminal-refresh-interval', 'n_intervals'),
        State('create-terminal', 'value'),
    )
    def update_terminal(n, current_value):
        logCMD = '''
             var textarea = document.getElementById('create-terminal');
             textarea.scrollTop = textarea.scrollHeight;
             '''
        new_value = createPage.terminal.read()
        if current_value != new_value:
            return new_value, logCMD
        return no_update, ""

    @app.callback(
        Output('create-terminal-hidden-div', 'children'),
        Input('create-terminal-clear-button', 'n_clicks'),
    )
    def output_no_update(clear_terminal):
        button_clicked = ctx.triggered_id
        if button_clicked == 'create-terminal-clear-button' and clear_terminal:
            createPage.terminal.clear()
        return html.Div()

    @app.callback(
        Output('create-button-createpage', 'disabled'),
        Input('create-check-trigger', 'children'),
        State('create-button-createpage', 'disabled'),
    )
    def button_state(trigger, buttonDisabled):
        return not buttonDisabled
        

    @app.callback(
        Output('create-check-trigger', 'children'),
        Input('app-name-input-createpage', 'value'),
        Input('app-location-input-createpage', 'value'),
        Input('app-template-input-createpage', 'value'),
        State('create-button-createpage', 'disabled'),
    )
    def button_state(appName, appLoc, appTmp, buttonIsDisabled):
        if appLoc:
            if appName and os.path.exists(appLoc) and appTmp:
                return 'False' if buttonIsDisabled else no_update
        return 'True' if not buttonIsDisabled else no_update
        

    app.clientside_callback(
        ClientsideFunction(namespace="my_clientside_library",
                        function_name="confetti_onclick"),
        Output("hidden-confetti-div", "children"),
        Input("create-app-successful-trigger", "children"),
    )

    @app.callback(
        Output('notifications-container-app-create', 'children'),
        Output('create-app-successful-trigger', 'children'),
        Input('create-button-createpage', 'n_clicks'),
        State('app-name-input-createpage', 'value'),
        State('app-location-input-createpage', 'value'),
        State('app-template-input-createpage', 'value'),
    )
    def create_app(create_button, appName, appDir, appTemplate:str):
        button_clicked = ctx.triggered_id
        if button_clicked == 'create-button-createpage' and create_button:
            app_path = pathlib.Path(appDir).joinpath(appName).resolve()
            if os.path.exists(app_path):
                class Error:
                    filepath = app_path
                return alerts.render('FileAlreadyExists', props=Error()), no_update
            def run():
                os.system(f"dashtools init {appName} {appTemplate} --dir {appDir} --no-update-check --silent")
            threading.Thread(target=run, daemon=True).run()
            createPage.terminal.writeln(f'$ Created new app {appName} at {app_path} with {appTemplate.capitalize()} template!')
            return alerts.render('AppCreateSuccess'), html.Div('triggered')
        return no_update, no_update
        
    @app.callback(
        Output('preview-output', 'children'),
        Output('notifications-container-app-preview', 'children'),
        Output('preview-tab-title', 'children'),
        Input('app-template-input-createpage', 'value'),
    )
    def preview_app(template:str):
        template_preview = buildApp.try_get_template_preview(template)
        object = template_preview.object
        alert = None
        title = f"Preview - {template.capitalize()} Template"
        if not template_preview.object:
            if template_preview.needs_module:
                createPage.terminal.writeln(f"$ You must install module '{template_preview.needs_module}' to preview app with the {template.capitalize()} template!")
            object = dmc.Center([
            html.H3("No Preview Available", style={
                    'opacity': '10%', 'padding-top': '50px'})
            ])
            alert = alerts.render('ModuleNotFound', props=template_preview) if template_preview.needs_module is not None else None
        return object, alert, title

    @app.callback(
        Output('app-settings-name-status', 'children'),
        Input('app-name-input-createpage', 'value')
    )
    def save_app_name(app_name):
        if app_name and ' ' not in app_name:
            return [dmc.Tooltip(
                label=f"Looks great! Your app with be created using this name.",
                withArrow=True,
                multiline=True,
                width=220,
                children=[
                    DashIconify(icon='bi:check-circle',
                                width=30, color='green')
                ])]
        else:
            return [dmc.Tooltip(
                label="Enter an app name you would like to use. The name cannot contain spaces.",
                withArrow=True,
                multiline=True,

                width=220,
                children=[
                    DashIconify(icon='bi:three-dots',
                                width=30, color='gray')
                ])]

    @app.callback(
        Output('app-settings-location-status', 'children'),
        Input('app-location-input-createpage', 'value'),
        prevent_initial_call=False
    )
    def save_app_name(path):
        if os.path.exists(path):
            return [dmc.Tooltip(
                label=f"Filepath found. Your application will be created here.",

                withArrow=True,
                multiline=True,
                width=220,
                children=[
                    DashIconify(icon='bi:check-circle',
                                width=30, color='green')
                ])]
        else:
            return [dmc.Tooltip(
                label="Enter a valid directory to create your application at.",
                withArrow=True,
                multiline=True,
                width=220,
                children=[
                    DashIconify(icon='bi:three-dots',
                                width=30, color='gray')
                ])]