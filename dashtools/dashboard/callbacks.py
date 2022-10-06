import os
import pathlib
from dash import Dash, Input, Output, State, no_update, html
import pages
import tree


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
        # pages.deploy.terminal.command('ls')
        new_value = pages.deploy.terminal.read()
        if current_value != new_value:
            return new_value, logCMD
        return no_update, ""

    @app.callback([
        Output('file-explorer-output', 'value'),
        Output('file-explorer-input', 'required'),
    ],
        Input('file-explorer-button', 'n_clicks'),
        State('file-explorer-input', 'value')
    )
    def update_output(n, filepath: os.PathLike):
        if not n:
            # Initial callbacks
            return html.Div(), False
        children = []
        if filepath:
            children = tree.tree(filepath)
            # if os.path.isdir(filepath):
            #     children = [str(x) for x in list(pathlib.Path(".").rglob("*"))]

        # TODO implement something like this
        # https://www.cssscript.com/folder-tree-json/
        return '\n'.join(children), True
