# Returns a preview of the template, used for dashtools UI
import dash_bootstrap_components as dbc
from dash import html

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "height":"440px"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

def render():
    sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", active="exact", style= { "cursor": "pointer" }),
                dbc.NavLink("Page 1", active="exact", style= { "cursor": "pointer" }),
                dbc.NavLink("Page 2", active="exact", style= { "cursor": "pointer" }),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style=SIDEBAR_STYLE,
    )

    # content = html.Div(id="page-content", style=CONTENT_STYLE)

    return  html.Div([sidebar])
