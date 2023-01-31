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

terminal = Terminal()

def render():
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
                              "height": "160px",
                              "resize": "none",
                              'font-size': '14px',
                              'font-family': 'Courier Bold',
                              'background-color': '#000000',
                              'color': '#ffffff',
                          })
        ],
    )

def generate_callbacks(app: Dash):
    @ app.callback(
        [
            Output('create-terminal', 'value'),
            Output('create-terminal-runjs', 'run'),
        ],
        Input('create-terminal-refresh-interval', 'n_intervals'),
        State('create-terminal', 'value'),
    )
    def update_terminal(n, current_value):
        logCMD = '''
             var textarea = document.getElementById('create-terminal');
             textarea.scrollTop = textarea.scrollHeight;
             '''
        new_value = createPage.terminal.read()
        if current_value != new_value:
            return new_value, logCMD
        return no_update, ""