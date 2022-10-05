import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import visdcc
from dash import dcc, html
from dash_iconify import DashIconify


class Terminal:
    def __init__(self) -> None:
        self.value = ''

    def read(self):
        return self.value

    def clear(self):
        self.value = ''

    def writeln(self, message):
        self.value = f'{self.value}\n{message}'


# Global terminal for user session
terminal = Terminal()


def file_explorer():
    return html.Div([
        dmc.Text('File Explorer'),
        html.Div([
            dmc.Space(h=5),
            dcc.Upload(
                # https://www.dash-mantine-components.com/components/button
                dmc.Button(
                    [
                        DashIconify(
                            icon='ant-design:file-add-outlined', width=30),
                        dmc.Text('Open File', inline=True,
                                 size='md', weight='bold')
                    ],
                    variant='subtle',
                    style={'color': 'inherit', 'text-decoration': 'none'},
                )
            )

        ], style={'width': '100%', 'height': '200px', 'text-align': 'center', 'background-color': 'red'})
    ])


def deploy_info():
    return html.Div([
        dmc.Text('Deployment Information'),
        dmc.Space(h=5),
        html.Div(
            [
                dmc.Tooltip(
                    label="This is a tooltip",
                    position="left",
                    placement="center",
                    gutter=10,
                    children=[
                        dmc.Checkbox(
                            id="checkbox",
                            label="File Exists: app.py",
                            checked=True,
                            disabled=True,
                            color="green")
                    ],
                    style={'padding-bottom': '10px'}
                ),
                dmc.Tooltip(
                    label="This is a tooltip",
                    position="left",
                    placement="center",
                    gutter=10,
                    children=[
                        dmc.Checkbox(
                            id="checkbox",
                            label="File Exists: Procfile",
                            checked=True,
                            disabled=True,
                            color="green")
                    ],
                    style={'padding-bottom': '10px'}
                ),
                dmc.Tooltip(
                    label="This is a tooltip",
                    position="left",
                    placement="center",
                    gutter=10,
                    children=[
                        dmc.Checkbox(
                            id="checkbox",
                            label="File Exists: requirements.txt",
                            checked=True,
                            disabled=True,
                            color="green")
                    ],
                    style={'padding-bottom': '10px'}
                ),
                dmc.Tooltip(
                    label="This is a tooltip",
                    position="left",
                    placement="center",
                    gutter=10,
                    children=[
                        dmc.Checkbox(
                            id="checkbox",
                            label="File Exists: runtime.txt",
                            checked=False,
                            disabled=True,
                            color="green")
                    ],
                    style={'padding-bottom': '10px'}
                ),
                dmc.Tooltip(
                    label="This is a tooltip",
                    position="left",
                    placement="center",
                    gutter=10,
                    children=[
                        dmc.Checkbox(
                            id="checkbox",
                            label="server = app.server",
                            checked=False,
                            disabled=True,
                            color="green")
                    ],
                    style={'padding-bottom': '10px'}
                ),
                dmc.Tooltip(
                    label="This is a tooltip",
                    position="left",
                    placement="center",
                    gutter=10,
                    children=[
                        dmc.Checkbox(
                            id="checkbox",
                            label="App Name Available",
                            checked=False,
                            disabled=True,
                            color="green")
                    ],
                    style={'padding-bottom': '10px'}
                ),
            ]
        )
    ], style={"height": 'auto', "width": 300, "overflow": "auto"})


def terminal_box():
    return html.Div(
        [
            visdcc.Run_js(id='deploy-terminal-runjs', run=""),
            dcc.Interval(id='deploy-terminal-refresh-interval',
                         interval=1000, n_intervals=0, disabled=False),
            dmc.Text('Terminal'),
            dmc.Space(h=5),
            html.Textarea(id='deploy-terminal',
                          contentEditable="false",
                          readOnly='true',
                          draggable='false',
                          style={
                              "width": "100%",
                              "height": "150px",
                              "resize": "none",
                              'font-size': '18px',
                              'background-color': '#000000',
                              'color': '#ffffff',
                          })
        ]
    )


def render():

    return html.Div(
        [
            dbc.Row([file_explorer()]),
            dbc.Row([deploy_info()]),
            dbc.Row([terminal_box()]),
        ],
        style={"background-color": "#aaaaaa",
               "height": "90vh", "padding": "10px"}
    )
