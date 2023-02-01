'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-10-23 14:52:57
'''


import sys
from dash import Dash, Input, Output, State, no_update, ctx, html
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
        if appName and appLoc and appTmp:
            return 'False' if buttonIsDisabled else no_update
        return 'True' if not buttonIsDisabled else no_update
        
    @app.callback(
        Output('create-terminal-hidden-div2', 'children'),
        Input('create-button-createpage', 'n_clicks'),
        State('app-name-input-createpage', 'value'),
        State('app-location-input-createpage', 'value'),
        State('app-template-input-createpage', 'value'),
    )
    def create_app(create_button, appName, appDir, appTemplate:str):
        button_clicked = ctx.triggered_id
        if button_clicked == 'create-button-createpage' and create_button:
            def run():
                import os
                os.system(f"dashtools init {appName} {appTemplate} --dir {appDir}")
            threading.Thread(target=run, daemon=True).run()
            createPage.terminal.writeln(f'$ Created new app {appName} at {appDir} with {appTemplate.capitalize()} template!')
        return html.Div()
        
    @app.callback(
        Output('preview-output', 'children'),
        Output('notifications-container-app-preview', 'children'),
        Input('app-template-input-createpage', 'value'),
    )
    def preview_app(template:str):
        template_preview = buildApp.try_get_template_preview(template)
        if not template_preview.object:
            alert = alerts.render('ModuleNotFound', props=template_preview)
            if template_preview.needs_module:
                createPage.terminal.writeln(f"$ You must install module '{template_preview.needs_module}' to preview app with the {template.capitalize()} template!")
            return dmc.Center([
            html.H3("Preview Not Found", style={
                    'opacity': '10%', 'padding-top': '50px'})
            ]), alert if template_preview.needs_module is not None else None
        return template_preview.object, None
