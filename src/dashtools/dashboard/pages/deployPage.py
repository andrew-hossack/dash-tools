import os
from typing import Union

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import visdcc
from dash import dcc, html
from dash_iconify import DashIconify


class FileExplorer:
    def __init__(self) -> None:
        self._deployReady = False  # Ready to upload
        self.appName = None
        self.root: os.PathLike = None
        self.requirementsExists = False
        self.renderYamlExists = False
        self.serverHookExists = False
        self.githubUrl = None
        self.deployReadyFlagCallback = False  # Only to be set by callback

    def setGithubUrl(self, config_remote_origin_url_raw: str):
        if not config_remote_origin_url_raw:
            self.githubUrl = None
            return
        remote_url = config_remote_origin_url_raw.replace(
            'git@github.com:', '').replace('https://github.com/', '').replace('.git', '')
        self.githubUrl = f'https://github.com/{remote_url}'

    def isDeployReady(self) -> bool:
        """ returns if app is ready to be deployed """
        if self.appName and self.root and self.requirementsExists and self.renderYamlExists and self.serverHookExists and self.githubUrl:
            return True
        return False

    def isDeployReadyWithStatus(self) -> Union[bool, dict]:
        """
        returns if app is ready to be deployed
        returns a list of items with their status
        """
        status = {
            "render app name": self.appName is not None,
            "src/app.py file": self.root is not None,
            "requirements.txt file": self.requirementsExists,
            "render.yaml file": self.renderYamlExists,
            "server=app.server code in src/app.py": self.serverHookExists,
            "project is pushed to public github": self.githubUrl is not None,
        }
        if self.isDeployReady():
            return status
        return (False, status)


# Global fileExplorerInstance for user session
fileExplorerInstance = FileExplorer()


def deploy_controller():
    return html.Div([
        dmc.Text('App Control'),
        dmc.Stack([
            dmc.Center([
                dmc.Text("Deployment readiness: "),
                dmc.Group(
                    build_checkbox('PENDING', '**Not Ready**',
                                   'Open a dash app in File Explorer to check deployment readiness', 'pending-deploy-status-id', text_margin_l='5px', tooltip_pos='top'),
                    id='deployment-readiness-status-output',
                    style={'margin-top': '17px', 'margin-left': '10px'}
                )
            ],
                style={'margin-top': '-14px', 'margin-bottom': '-25px'}),
            dmc.Center(
                [
                    dmc.Button(
                        'Deploy',
                        variant="gradient",
                        leftIcon=[
                            html.Img(
                                src='https://render.com/images/deploy-to-render-button.svg', alt="Deploy to Render")
                        ],
                        disabled=True,
                        style={'width': '200px', 'opacity': '0.6'},
                        id='app-control-deploy-button')
                ],
                id='app-control-deploy-button-container',
                style={'margin-bottom': '-10px'}
            )
            # ]),
        ], style={'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', "height": '106px', 'padding': '10px'})
    ], style={"width": '100%'})


class Terminal():
    def __init__(self) -> None:
        self.value = '$ Select a dash project in File Explorer to deploy your app to Render.com ...'

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
        html.Div(id='readiness-check-trigger', style={'display': 'none'}),
        dcc.Interval(id='file-explorer-refresh-interval',
                     interval=1000, n_intervals=0, disabled=True),
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
            html.Div(id='update-filetree-hidden',
                     style={'display': 'none'}),
            html.Div(
                id='file-explorer-output',
                style={'width': '100%', 'height': '350px', 'margin-top': '-16px'}
            )
        ], style={'height': '460px', 'width': '100%', 'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', 'overflow': 'clip', 'min-width':'400px'})
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
                withArrow=True,
                multiline=True,
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


def build_checkbox(status: str, text: str, tooltip: str, tooltip_id: str, text_margin_l='10px', tooltip_pos='left') -> html.Div:
    """ status: 'PASS' or 'FAIL' or 'PENDING' """
    return html.Div([
        html.Div(dmc.Tooltip(
            id=tooltip_id,
            children=html.Div(ReadinessStatus(status).get()),
            label=tooltip,
            position=tooltip_pos,
            withArrow=True,
            multiline=True,
            width=220), style={'display':'inline-block'}),
        dcc.Markdown(text, style={'margin-bottom': '2px',
                                  'margin-left': text_margin_l, 'display': 'inline-block'}),
    ])


def deploy_info():
    return html.Div([
        dmc.Text('Deployment Requirements'),
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
                            'readiness-check-render-yaml-generator-button', 'Generate render.yaml', 'readiness-check-render-yaml-generator-vis').get()
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
                            'readiness-check-requirements-generator-button', 'Generate requirements.txt', 'readiness-check-requirements-generator-vis').get()
                    ]),
                dmc.Group(
                    [
                        build_checkbox(
                            'PENDING',
                            'Project Requirement: **Pushed to GitHub**',
                            'Your project directory must be pushed to Github in a public git repo',
                            'readiness-check-on-github'
                        )
                    ]),
                dmc.Group(
                    build_checkbox(
                        'PENDING',
                        'Code exists: `server = app.server` in **src/app.py**',
                        'server = app.server hook must be exposed in src/app.py to deploy to Render.com',
                        'readiness-check-hook-exists'
                    )),
                # dmc.Divider(variant="dotted"),
                dmc.Divider(variant="dotted", style={
                    'margin-left': '60px', 'margin-right': '60px'}),
                dmc.Group(
                    [
                        html.Div(
                            dmc.Tooltip(
                                label="Generate random name",
                                withArrow=True,
                                multiline=True,
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
                            style={'margin-top': '-33px',
                                   'margin-right': '-5px',
                                   'margin-left': '1px'}
                        ),
                        dmc.TextInput(
                            label="Render App Name",
                            style={"width": '360px', 'margin-right': '10px'},
                            id='app-control-name-input',
                            placeholder='Web Name; eg. my-example-app'),
                        html.Div(
                            dmc.Tooltip(
                                label="Enter an app name you would like to use. Render may change this name if it is not unique.",
                                withArrow=True,
                                multiline=True,
                                width=220,
                                children=[
                                    DashIconify(icon='bi:three-dots',
                                                width=30, color='gray')
                                ]),
                            id='app-control-name-status', style={'margin-top': '25px'}),
                    ],
                    style={'margin-top': '10px', 'margin-bottom': '12px'}
                )

            ], style={'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', "height": 'auto', 'padding': '10px', 'min-width':'500px'}
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
                            withArrow=True,
                            multiline=True,
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
                              "height": "230px",
                              "resize": "none",
                              'font-size': '14px',
                              'font-family': 'Courier Bold',
                              'background-color': '#000000',
                              'color': '#ffffff',
                          })
        ],
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
            dbc.Row([terminal_box()], style={'padding-top': '20px'}),
        ],
        style={"height": "90vh", "padding": "10px", 'width':'auto'}
    )
