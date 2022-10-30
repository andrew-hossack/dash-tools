'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-10-23 14:52:57
'''


from dash import Dash, Input, Output, State, no_update, ctx, html
try:
    from dashtools.dashboard.pages import createPage
except ModuleNotFoundError:
    from ..pages import createPage


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
        Input('create-terminal-clear-button', 'n_clicks')
    )
    def deploy_button(clear_terminal):
        button_clicked = ctx.triggered_id
        if button_clicked == 'create-terminal-clear-button' and clear_terminal:
            createPage.terminal.clear()
        return html.Div()
