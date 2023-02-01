# Returns a preview of the template, used for dashtools UI
import dash_bootstrap_components as dbc
from dash import dcc, html

def render():
    return dbc.Container(
        [
            dcc.Store(id="store"),
            html.H2("Sidebar App"),
            html.Hr(),
            dbc.Tabs(
                [
                    dbc.Tab([
                        "Tab 1 Content"
                    ],label="Scatter", tab_id="scatter"),
                    dbc.Tab([
                        "Tab 2 Content"
                    ],
                    label="Histograms", tab_id="histogram"),
                ],
                id="tabs",
                active_tab="scatter",
            ),
            html.Div(id="tab-content", className="p-4"),
        ]
    )