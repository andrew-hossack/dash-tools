import os
import subprocess

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import visdcc
from dash import dcc, html
from dash_iconify import DashIconify


class HerokuApplication:
    def __init__(self) -> None:
        self._ready = False  # Ready to upload
        self.appName = None
        self.root: os.PathLike = None

    def isDeployReady(self) -> bool:
        """ Flag to tell if deploy is ready """
        # TODO if x and y and z:
        return self._ready


# Global herokuApplication for user session
herokuApplication = HerokuApplication()


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
                        style={'width': '200px'},
                        id='app-control-deploy-button'),
                ]
            ),
        ], style={'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', "height": '275px', 'padding': '10px'})
    ], style={"width": '100%', "overflow": "auto"})


class Terminal():
    def __init__(self) -> None:
        self.value = ''
    #     threading.Thread.__init__(self)
    #     self.cmd = None

    # def command(self, cmd: str):
    #     self.cmd = cmd
    #     self.start()

    #     self.join()
    #     self.cmd = None

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
        # dmc.Stack()
        dmc.Text('File Explorer'),
        # dmc.Center([
        dmc.Stack([
            dmc.Center([
                # dcc.Upload(
                # https://www.dash-mantine-components.com/components/button
                dmc.TextInput(
                    placeholder="App Path; eg. /Users/Andrew/MyDashApp",
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
        html.Div(
            [
                dbc.Row(
                    dmc.Tooltip(
                        label="This is a tooltip",
                        position="left",
                        placement="center",
                        withArrow=True,
                        wrapLines=True,
                        width=220,
                        zIndex=99999,
                        gutter=0,
                        children=[
                            dmc.Checkbox(
                                id="readiness-check-app-exists",
                                label="File Exists: app.py",
                                checked=False,
                                disabled=True,
                                color="green")
                        ],
                        style={'margin-bottom': '10px',
                               'margin-bottom': '10px'}
                    ), style={'padding': '1px'}),
                dbc.Row(
                    dmc.Tooltip(
                        label="This is a tooltip",
                        position="left",
                        placement="center",
                        withArrow=True,
                        wrapLines=True,
                        width=220,
                        zIndex=99999,
                        gutter=0,
                        children=[
                            dmc.Checkbox(
                                id="readiness-check-procfile-exists",
                                label="File Exists: Procfile",
                                checked=False,
                                disabled=True,
                                color="green")
                        ],
                        style={'margin-bottom': '10px',
                               'margin-bottom': '10px'}
                    ), style={'padding': '1px'}),
                dbc.Row(
                    dmc.Tooltip(
                        label="This is a tooltip",
                        position="left",
                        placement="center",
                        withArrow=True,
                        wrapLines=True,
                        width=220,
                        zIndex=99999,
                        gutter=0,
                        children=[
                            dmc.Checkbox(
                                id="readiness-check-requirements-exists",
                                label="File Exists: requirements.txt",
                                checked=False,
                                disabled=True,
                                color="green")
                        ],
                        style={'margin-bottom': '10px',
                               'margin-bottom': '10px'}
                    ), style={'padding': '1px'}),
                dbc.Row(
                    dmc.Tooltip(
                        label="This is a tooltip",
                        position="left",
                        placement="center",
                        withArrow=True,
                        wrapLines=True,
                        width=220,
                        zIndex=99999,
                        gutter=0,
                        children=[
                            dmc.Checkbox(
                                id="readiness-check-runtime-exists",
                                label="File Exists: runtime.txt",
                                checked=False,
                                disabled=True,
                                color="green")
                        ],
                        style={'margin-bottom': '10px',
                               'margin-bottom': '10px'}
                    ), style={'padding': '1px'}),
                dbc.Row(
                    dmc.Tooltip(
                        label="This is a tooltip",
                        position="left",
                        placement="center",
                        withArrow=True,
                        wrapLines=True,
                        width=220,
                        zIndex=99999,
                        gutter=0,
                        children=[
                            dmc.Checkbox(
                                id="readiness-check-hook-exists",
                                label="Procfile is correct and server = app.server exists TODO split",
                                checked=False,
                                disabled=True,
                                color="green")
                        ],
                        style={'margin-bottom': '10px',
                               'margin-bottom': '10px'}
                    ), style={'padding': '1px'}),
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
                              "height": "200px",
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
