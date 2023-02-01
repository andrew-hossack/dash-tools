from dash import html, dcc, Dash
import dash_bootstrap_components as dbc
import visdcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from dashtools.templating import Templates, buildApp

class Terminal():
    def __init__(self) -> None:
        self.value = '$ Create a new dash application. Choose app name, template and location to create your project ...'

    def read(self):
        return self.value

    def clear(self):
        self.value = ''

    def writeln(self, message):
        message = str(message)
        if self.value != '':
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
            html.Div(id='create-terminal-hidden-div2',
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
                              "margin-top":"-4px",
                              "height": "260px",
                              "resize": "none",
                              'font-size': '14px',
                              'font-family': 'Courier Bold',
                              'background-color': '#000000',
                              'color': '#ffffff',
                          })
        ],
    )


def preview_box():
    return html.Div([
        dmc.Text('Preview', id='preview-tab-title'),
        html.Div(
            id='preview-output',
            children=buildApp.try_get_template_preview('default').object, 
            style={'height': '460px', 'width': '100%', 'border-radius': '10px', 'border': '1px solid rgb(233, 236, 239)', 'overflow': 'clip', 'padding':'10px'}) # TODO need to figure out 'max-width':'575px'
    ], style={'margin-bottom':'10px'})


def create_box():
    return html.Div([
        dmc.Text('App Settings'),
        html.Div([
            dmc.Group([
                dmc.TextInput(
                    id='app-name-input-createpage',
                    label="App Name",
                    style={"width": '360px', 'margin-right': '10px'},
                    placeholder='App Filename; eg. MyApp'),
                html.Div(
                    dmc.Tooltip(
                        id='app-settings-name-status',
                        label="Enter an app name you would like to use. The name cannot contain spaces.",
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
                    label="Create Location",
                    id='app-location-input-createpage',
                    style={"width": '360px', 'margin-right': '10px'},
                    placeholder='App Path; eg. /Users/MyApp'),
                html.Div(
                    dmc.Tooltip(
                        id='app-settings-location-status',
                        label="Enter a valid directory to create your application at.",
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
                        id='app-template-input-createpage',
                        value="default",
                        data=sorted([
                            {"value": template.value, "label": str.capitalize(template.value)} for template in Templates.Template
                        ], key=lambda x: x['label']),
                        style={"width": 200, "marginBottom": 10},
                    ),
                    dmc.Text(id="selected-value"),
                ]
            ),
            dmc.Button(
                'Create',
                id='create-button-createpage',
                variant="gradient",
                leftIcon=[
                    DashIconify(icon='gridicons:create',
                                width=20, color='light-gray')
                ],
                disabled=True,
                style={'width': '200px', 'opacity': '1.0'},
            )
        ], style={
            'height': '265px',
            'width': '100%',
            'border-radius': '10px',
            'border': '1px solid rgb(233, 236, 239)',
            'overflow': 'clip',
            'padding-left':'20px',
            'padding-right':'20px',
            'padding-top':'10px',
            'min-width':'460px',
        })
    ])


def render():
    return html.Div(
        [
            html.Div(id='create-check-trigger', style={'display': 'none'}),
            dbc.Row(preview_box()),
            dbc.Row([
                dbc.Col(create_box()),
                dbc.Col(terminal_box()),
            ]),
        ],
        style={"height": "90vh", "padding": "10px"}
    )


if __name__ == "__main__":
    app = Dash()
    app.layout = render()
    app.run_server(debug=True)
