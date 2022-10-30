from dash import html, dcc, Dash
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


def preview_box():
    return html.Div([
        dmc.Text('Preview'),
        html.Div([
            dmc.Group("Foo"),
            dmc.Group("Bar"),
        ], style={'height': '460px', 'width': '100%', 'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', 'overflow': 'clip'})
    ])


def create_box():
    return html.Div([
        dmc.Text('App Settings'),
        html.Div([
            dmc.Group([
                dmc.TextInput(
                    label="App Name",
                    style={"width": '360px', 'margin-right': '10px'},
                    placeholder='App Filename; eg. my-app'),
                html.Div(
                    dmc.Tooltip(
                        label="Enter an app name you would like to use. Render may change this name if it is not unique.",
                        placement="center",
                        withArrow=True,
                        wrapLines=True,
                        width=220,
                        children=[
                            DashIconify(icon='bi:three-dots',
                                        width=30, color='gray')
                        ]),
                    style={'margin-top': '25px'})
            ]),
            dmc.Group([
                dmc.TextInput(
                    label="File Location",
                    style={"width": '360px', 'margin-right': '10px'},
                    placeholder='Location To Create App; eg. ~/Desktop'),
                html.Div(
                    dmc.Tooltip(
                        label="Enter an app name you would like to use. Render may change this name if it is not unique.",
                        placement="center",
                        withArrow=True,
                        wrapLines=True,
                        width=220,
                        children=[
                            DashIconify(icon='bi:three-dots',
                                        width=30, color='gray')
                        ]),
                    style={'margin-top': '25px'})
            ]),
            dmc.Group(
                [
                    dmc.Select(
                        label="Template",
                        placeholder="Select one",
                        id="framework-select",
                        value="ng",
                        data=[
                            {"value": "react", "label": "React"},
                            {"value": "ng", "label": "Angular"},
                            {"value": "svelte", "label": "Svelte"},
                            {"value": "vue", "label": "Vue"},
                        ],
                        style={"width": 200, "marginBottom": 10},
                    ),
                    dmc.Text(id="selected-value"),
                ]
            ),
            dmc.Center(
                [
                    dmc.Button(
                        'Create',
                        variant="gradient",
                        leftIcon=[
                            DashIconify(icon='gridicons:create',
                                        width=20, color='light-gray')
                        ],
                        disabled=True,
                        style={'width': '200px', 'opacity': '1.0'},
                    )
                ],
                style={'margin-bottom': '-10px'}
            ),
        ], style={'height': '460px', 'width': '100%', 'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', 'overflow': 'clip'})
    ])


def render():
    terminal.writeln('$ Create a new Dash Application')
    return html.Div(
        [
            dmc.Center([
                DashIconify(icon='emojione:hammer-and-wrench',
                            width=35, color='light-gray', style={'margin-right': '20px'}),
                dmc.Title(["Under Construction"], order=1),
                DashIconify(icon='emojione:hammer-and-wrench',
                            width=35, color='light-gray', style={'margin-left': '20px'})
            ]),
            # dbc.Row([
            #     dbc.Col(preview_box()),
            #     dbc.Col(create_box()),
            # ]),
            # dbc.Row(terminal_box(), style={'padding-top': '20px'}),
        ],
        style={"height": "90vh", "padding": "10px"}
    )


if __name__ == "__main__":
    app = Dash()
    app.layout = render()
    app.run_server(debug=True)
