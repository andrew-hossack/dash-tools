# Returns a preview of the template, used for dashtools UI
import dash_bootstrap_components as dbc
from dash import dcc, html
import dash_mantine_components as dmc
import os

def render():
    return dbc.Container(
        [
            dcc.Store(id="store"),
            html.H2("Tabs App Template"),
            html.Hr(),
            dbc.Tabs(
                [
                    dbc.Tab([
                        dmc.Image(
                            src=os.path.normpath("/assets/golden-retriever-dog.jpeg"), alt="dogs", width=400
                        )
                    ],label="Dogs", tab_id="scatter"),
                    dbc.Tab([
                        dmc.Image(
                            src=os.path.normpath("/assets/four-cute-cats.jpeg"), alt="cats", width=400
                        )
                    ],
                    label="Cats", tab_id="histogram"),
                ],
                id="tabs",
                active_tab="scatter",
            ),
            html.Div(id="tab-content", className="p-4"),
        ]
    )