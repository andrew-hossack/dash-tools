# Returns a preview of the template, used for dashtools UI
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_mantine_components as dmc

def render():
    return html.Div([
        dmc.Alert(
        [
            "Hi from Dash Mantine Components. You can create some great looking dashboards using me!"
        ],
        title="Welcome!",
        color="violet",
        ),
        dmc.Text('Visit https://www.dash-mantine-components.com/getting-started for more information!')
    ])