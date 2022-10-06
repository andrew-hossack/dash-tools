import subprocess
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import visdcc
from dash import dcc, html
from dash_iconify import DashIconify


class Terminal:
    def __init__(self) -> None:
        self.value = ''

    def command(self, cmd: str):
        """ Write a command to be run in subprocess """
        # TODO spin up new thread to run commands
        # https://stackoverflow.com/questions/4514751/pipe-subprocess-standard-output-to-a-variable
        self.writeln(f'$ {cmd}')
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.writeln(proc.stdout.read().decode('ascii'))
        except Exception as e:
            self.writeln(e)

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


def file_explorer():
    return html.Div([
        # dmc.Stack()
        dmc.Text('File Explorer'),
        # dmc.Center([
        dmc.Stack([
            dmc.Center([
                # dcc.Upload(
                # https://www.dash-mantine-components.com/components/button
                dmc.TextInput(
                    placeholder="Path to Your Application; eg. /Users/Andrew/MyDashApp",
                    style={"width": 400},
                    id="file-explorer-input",
                    radius=5),
                dmc.Space(w=10),
                dmc.Button(
                    [
                        DashIconify(
                            icon='ant-design:file-add-outlined', width=30),
                        dmc.Text('Open File', inline=True,
                                 size='md', weight='bold')
                    ],
                    variant='subtle',
                    color='gray',
                    style={'color': 'gray', 'text-decoration': 'none'},
                    id='file-explorer-button'
                )
            ], style={'padding-top': '15px'}),
            dmc.Divider(variant="dotted", style={
                        'margin-left': '60px', 'margin-right': '60px'}),
            html.Textarea(
                id='file-explorer-output',
                contentEditable="false",
                readOnly='true',
                draggable='false',
                style={
                    'width': '100%',
                    'height': '400px',
                    '-moz-user-select': 'none',
                    '-khtml-user-select': 'none',
                    '-webkit-user-select': 'none',
                    '-ms-user-select': 'none',
                    'user-select': 'none',
                    "resize": "none",
                    'border': 'none',
                    'outline': 'none'})
            # ])
        ], style={'width': '100%', 'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)'})
    ])


def deploy_info():
    return html.Div([
        dmc.Text('Deployment Readiness'),
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
            ],
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
                              'font-size': '14px',
                              'font-family': 'Courier Bold',
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
        style={"height": "90vh", "padding": "10px"}
    )
