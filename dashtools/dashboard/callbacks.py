from dash import Dash, Input, Output, State, no_update
import pages


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
        new_value = pages.deploy.terminal.read()
        if current_value != new_value:
            return new_value, logCMD
        return no_update, ""
