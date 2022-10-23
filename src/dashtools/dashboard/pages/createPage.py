from dash import html, dcc
import dash_bootstrap_components as dbc
import visdcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify


class Terminal():
    def __init__(self) -> None:
        self.value = ''

    def read(self):
        return self.value

    def clear(self):
        self.value = ''

    def writeln(self, message):
        message = str(message)
        if self.value is not '':
            self.value = f'{self.value}\n{message}'
        else:
            self.value = message


# Global terminal for user session
terminal = Terminal()


def terminal_box():
    return html.Div(
        [
            html.Div(id='create-terminal-hidden-div',
                     style={'display': 'none'}),
            visdcc.Run_js(id='create-terminal-runjs', run=""),
            dcc.Interval(id='create-terminal-refresh-interval',
                         interval=500, n_intervals=0, disabled=False),
            dbc.Row(
                [
                    dmc.Text('Command Output'),
                    html.Div(
                        dmc.Tooltip(
                            label="Clear",
                            placement="center",
                            withArrow=True,
                            wrapLines=True,
                            children=[
                                html.Button(
                                    DashIconify(icon='codicon:clear-all',
                                                width=18, color='black'),
                                    style={
                                        "background": "none",
                                        "color": "inherit",
                                        "border": "none",
                                        "padding": "0",
                                        "margin": "0",
                                        "font": "inherit",
                                        "cursor": "pointer",
                                        "outline": "inherit",
                                    },
                                    id='create-terminal-clear-button'
                                )
                            ]),
                        style={'margin-top': '-26px', 'margin-left': '136px'}
                    ),
                ]
            ),
            dmc.Space(h=5),
            html.Textarea(id='create-terminal',
                          contentEditable="false",
                          readOnly='true',
                          draggable='false',
                          style={
                              "width": "100%",
                              "height": "160px",
                              "resize": "none",
                              'font-size': '14px',
                              'font-family': 'Courier Bold',
                              'background-color': '#000000',
                              'color': '#ffffff',
                          })
        ]
    )


def render():
    terminal.writeln('$ Create a new Dash Application')
    return html.Div(
        [
            # dbc.Row([
            #     dbc.Col(),
            #     dbc.Col()
            # ]),
            dbc.Row(terminal_box(), style={'padding-top': '20px'}),
        ],
        style={"height": "90vh", "padding": "10px"}
    )
