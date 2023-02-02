# Returns a preview of the template, used for dashtools UI
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def render():
    return html.Div([
        dmc.Alert(
        [
            "Hi from Dash Mantine Components. You can create some great looking dashboards using me!"
        ],
        title="Welcome!",
        color="violet",
        style={'margin-bottom':'20px'}
        ),
        
        dmc.List(
            icon=[dmc.ThemeIcon(
                DashIconify(icon="radix-icons:check-circled", width=16),
                radius="xl",
                color="teal",
                size=24,
            )],
            size="sm",
            spacing="sm",
            children=[
                dmc.ListItem("Check out the Mantine and DashTools Docs."),
                dmc.ListItem("Install python virtual environment."),
                dmc.ListItem(
                    dmc.Text(["Install DashTools with ", dmc.Code("pip install dash-tools")], style={'font-size':'14px'})
                ),
                dmc.ListItem(
                    dmc.Text(["Start the GUI with ", dmc.Code("dashtools gui")], style={'font-size':'14px'})
                ),
                dmc.ListItem(
                    "Explore and build amazing Dash apps.",
                    icon=[dmc.ThemeIcon(
                        DashIconify(icon="radix-icons:pie-chart", width=16),
                        radius="xl",
                        color="blue",
                        size=24,
                    )],
                ),
            ],
            style={'margin-bottom':'20px'}
        ),
        dmc.Text('Visit https://www.dash-mantine-components.com/getting-started for more information!')
    ])