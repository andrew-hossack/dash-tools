from dash import Output, Input, Dash
from time import time


def generate_callbacks(app: Dash):

    @app.callback(
        Output('deploy-terminal', 'srcDoc'),
        Input('deploy-terminal-refresh-interval', 'n_intervals'),
    )
    def update(n):
        return str(time())
