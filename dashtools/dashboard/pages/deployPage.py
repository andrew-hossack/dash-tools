import enum
import os
import random
import subprocess

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import visdcc
from dash import dcc, html
from dash_iconify import DashIconify


class FileExplorer:
    def __init__(self) -> None:
        self._ready = False  # Ready to upload
        self.appName = None
        self.root: os.PathLike = None

    def isDeployReady(self) -> bool:
        """ Flag to tell if deploy is ready """
        # TODO if x and y and z:
        return self._ready


# Global fileExplorerInstance for user session
fileExplorerInstance = FileExplorer()


def deploy_controller():
    return html.Div([
        dmc.Text('App Control'),
        dmc.Stack([
            dmc.Group(
                [
                    html.Div(
                        dmc.Tooltip(
                            label="Generate random name",
                            placement="center",
                            withArrow=True,
                            wrapLines=True,
                            children=[
                                html.Button(
                                    DashIconify(icon='ci:refresh',
                                                width=20, color='black'),
                                    style={
                                        "background": "none",
                                        "color": "inherit",
                                        "border": "none",
                                        "padding": "0",
                                        "margin": "0",
                                        "font": "inherit",
                                        "cursor": "pointer",
                                        "outline": "inherit",
                                    }
                                )
                            ]),
                        id='app-control-name-refresh',
                        style={'margin-top': '-33px', 'margin-right': '-10px'}
                    ),
                    dmc.TextInput(
                        label="Heroku App Name",
                        style={"width": '380px'},
                        id='app-control-name-input',
                        placeholder='Application Name; eg. my-example-app'),
                    html.Div(
                        dmc.Tooltip(
                            label="Enter an app name you would like to use.",
                            placement="center",
                            withArrow=True,
                            wrapLines=True,
                            width=220,
                            children=[
                                DashIconify(icon='bi:three-dots',
                                            width=40, color='gray')
                            ]),
                        id='app-control-name-status', style={'margin-top': '25px'}),
                ]
            ),
            dmc.Space(h=95),
            dmc.Divider(variant="dotted"),
            dmc.Center(
                [
                    dmc.Button(
                        'Run Local',
                        variant="gradient",
                        leftIcon=[DashIconify(
                            icon="bi:play")],
                        style={'width': '200px', 'margin-right': '50px'},
                        id='app-control-run-button'),
                    dmc.Button(
                        'Deploy',
                        variant="gradient",
                        leftIcon=[DashIconify(
                            icon="bi:cloud-upload")],
                        disabled=True,
                        style={'width': '200px'},
                        id='app-control-deploy-button'),
                ]
            ),
        ], style={'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', "height": '275px', 'padding': '10px'})
    ], style={"width": '100%', "overflow": "auto"})


class Terminal():
    def __init__(self) -> None:
        self.value = ''

    def command(self, cmd):
        """ Write a command to be run in subprocess """
        self.writeln(f'$ {cmd}')
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as proc:
            self.writeln(proc.stdout.read().decode('utf-8'))
            if proc.returncode != 0:
                self.writeln(proc.stderr.read().decode('utf-8'))

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
        dcc.Interval(id='file-explorer-refresh-interval',
                     interval=500, n_intervals=0, disabled=True),
        dmc.Text('File Explorer'),
        dmc.Stack([
            dmc.Center([
                dmc.TextInput(
                    placeholder="App Path; eg. /Users/MyApp",
                    style={"width": '100%'},
                    id="file-explorer-input",
                    radius=5),
                dmc.Space(w=10),
                dmc.Button(
                    [
                        DashIconify(
                            icon='ant-design:file-add-outlined', width=25),
                        dmc.Text('Open File', inline=True,
                                 size='md', weight='bold')
                    ],
                    variant='subtle',
                    color='gray',
                    style={'color': 'gray',
                           'text-decoration': 'none'},
                    id='file-explorer-button'
                )
            ], style={'padding-top': '15px', 'padding-right': '15px', 'padding-left': '15px'}),
            dmc.Divider(variant="dotted", style={
                        'margin-left': '60px', 'margin-right': '60px'}),
            html.Div(
                id='file-explorer-output',
                style={'width': '100%', 'height': '421px', 'margin-top': '-16px'}
            )
        ], style={'height': '492px', 'width': '100%', 'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', 'overflow': 'clip'})
    ])


class FileGenerator():
    def __init__(self, button_id: str, tooltip_label: str, visibility_id: str):
        """
        Args:
            button_id (str): Button uuid
            tooltip_label (str): Tooltip hover label
            visibility_id (str): Component ID for toggling generator visibility

        Usage:
            FileGenerator('foo-id').get()
        """
        self._uuid = button_id
        self._vis_id = visibility_id
        self._tooltip_lbl = tooltip_label

    def get(self) -> html.Div:
        return html.Div(
            dmc.Tooltip(
                label=self._tooltip_lbl,
                placement="center",
                withArrow=True,
                wrapLines=True,
                children=html.Button(
                    DashIconify(icon='ci:refresh',
                                width=16, color='black', style={'margin-bottom': '5px'}),
                    style={
                        "background": "none",
                        "color": "inherit",
                        "border": "none",
                        "font": "inherit",
                        "cursor": "pointer",
                        "padding": "0",
                        "outline": "inherit",
                        "margin-bottom": "15px",
                        'margin-left': '-5px',
                    },
                    id=self._uuid
                )
            ),
            style={'display': 'none'},
            id=self._vis_id
        )


class ReadinessStatus():
    def __init__(self, status: str):
        """
            Usage: ReadinessStatus('PASS').get()
            Args: status (str): 'PASS', 'FAIL', 'PENDING'
        """
        allowed_vals = ["PASS", "FAIL", "PENDING"]
        if status not in allowed_vals:
            raise ValueError(
                f'ReadinessStatus must be of type {allowed_vals}, not {status}')
        if status == "PASS":
            self._val = DashIconify(icon='clarity:check-circle-line',
                                    width=20, style={'margin-bottom': '2px', 'color': 'green'})
        elif status == "FAIL":
            self._val = DashIconify(icon='clarity:error-line',
                                    width=20, style={'margin-bottom': '2px', 'color': 'red'})
        elif status == "PENDING":
            self._val = DashIconify(icon='carbon:pending',
                                    width=15, style={'margin-bottom': '2px', 'color': 'gray', 'margin-left': '2px', 'margin-right': '3px'})

    def get(self) -> html.Div:
        return self._val


def build_checkbox(status: str, text: str, tooltip: str, tooltip_id: str) -> html.Div:
    """ status: 'PASS' or 'FAIL' or 'PENDING' """
    return html.Div([
        dmc.Tooltip(
            id=tooltip_id,
            children=ReadinessStatus(status).get(),
            label=tooltip,
            position="left",
            placement="center",
            withArrow=True,
            wrapLines=True,
            width=220),
        dcc.Markdown(text, style={'margin-bottom': '2px',
                                  'margin-left': '10px', 'display': 'inline-block'}),
    ])


def deploy_info():
    return html.Div([
        dmc.Text('Deployment Readiness'),
        html.Div(
            [
                dmc.Group(
                    build_checkbox(
                        'PENDING',
                        'File exists: **src/app.py**',
                        'app.py file must exist in the src/ directory',
                        'readiness-check-app-exists'
                    )),
                dmc.Group(
                    [
                        build_checkbox(
                            'PENDING',
                            'File exists: **render.yaml**',
                            'render.yaml file must be included to deploy to Render.com',
                            'readiness-check-render-yaml-exists'
                        ),
                        FileGenerator(
                            'readiness-check-render-yaml-generator', 'Generate render.yaml', 'readiness-check-render-yaml-generator-vis').get(),
                    ]),
                dmc.Group(
                    [
                        build_checkbox(
                            'PENDING',
                            'File exists: **requirements.txt**',
                            'requirements.txt file must be included to deploy to Render.com',
                            'readiness-check-requirements-exists'
                        ),
                        FileGenerator(
                            'readiness-check-requirements-generator', 'Generate requirements.txt', 'readiness-check-requirements-generator-vis').get(),
                    ]),
                dmc.Group(
                    build_checkbox(
                        'PENDING',
                        'Code exists: `server = app.server` in **src/app.py**',
                        'server = app.server hook must be exposed in src/app.py to deploy to Render.com',
                        'readiness-check-hook-exists'
                    )),
            ], style={'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', "height": 'auto', 'padding': '10px'}
        )
    ], style={"width": '100%', "overflow": "auto", "margin-bottom": "10px"})


def terminal_box():
    return html.Div(
        [
            visdcc.Run_js(id='deploy-terminal-runjs', run=""),
            dcc.Interval(id='deploy-terminal-refresh-interval',
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
                                    id='deploy-terminal-clear-button'
                                )
                            ]),
                        style={'margin-top': '-26px', 'margin-left': '136px'}
                    ),
                ]
            ),
            dmc.Space(h=5),
            html.Textarea(id='deploy-terminal',
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

    return html.Div(
        [

            dbc.Row([
                dbc.Col(file_explorer()),
                dbc.Col([
                    deploy_info(),
                    deploy_controller()
                ])
            ]),
            dbc.Row([terminal_box()], style={'padding-top': '10px'}),
        ],
        style={"height": "90vh", "padding": "10px"}
    )
