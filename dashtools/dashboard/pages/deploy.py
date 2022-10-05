from dash import html, dcc
import dash_bootstrap_components as dbc
import visdcc


ROW_STYLE = {'padding-left': '20px'}


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


def terminal_box():
    return html.Div(
        [
            visdcc.Run_js(id='deploy-terminal-runjs', run=""),
            dcc.Interval(id='deploy-terminal-refresh-interval',
                         interval=1000, n_intervals=0, disabled=False),
            html.Textarea(id='deploy-terminal',
                          contentEditable="false",
                          placeholder="Terminal Output (Empty)",
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
            dbc.Row(['Row1']),
            dbc.Row([
                terminal_box()
            ]),
        ],
        style={"background-color": "#aaaaaa",
               "height": "90vh", "padding": "10px"}
    )
