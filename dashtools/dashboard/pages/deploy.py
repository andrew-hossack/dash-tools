from time import time
from dash import html, Input, Output, dcc
import dash_bootstrap_components as dbc


ROW_STYLE = {'padding-left': '20px'}


class Terminal:
    def __init__(self) -> None:
        self.value = 'Init'

    def read(self):
        self.value = str(time())
        return self.value

    def clear(self):
        self.value = ''

    def writeln(self, message):
        self.value = f'{self.value}\n{message}'


# Global terminal for user session
terminal = Terminal()


def render():

    return html.H1(
        [
            dbc.Row(['Row1'], style=ROW_STYLE),
            dbc.Row([
                html.Div(
                    [
                        dcc.Interval(id='deploy-terminal-refresh-interval',
                                     interval=1000, n_intervals=0, disabled=False),
                        html.Iframe(id='deploy-terminal')
                    ]
                )
            ], style=ROW_STYLE),
        ],
        style={"background-color": "#ffffff"}
    )
