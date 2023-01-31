# Returns a preview of the template, used for dashtools UI
import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, dcc, html

def render():
    return dbc.Container(
        [
            dcc.Store(id="store"),
            html.H1("Dynamically rendered tab content - {appName}"),
            html.Hr(),
            dbc.Button(
                "Regenerate graphs",
                color="primary",
                id="button",
                className="mb-3",
            ),
            dbc.Tabs(
                [
                    dbc.Tab(label="Scatter", tab_id="scatter"),
                    dbc.Tab(label="Histograms", tab_id="histogram"),
                ],
                id="tabs",
                active_tab="scatter",
            ),
            html.Div(id="tab-content", className="p-4"),
        ]
    )