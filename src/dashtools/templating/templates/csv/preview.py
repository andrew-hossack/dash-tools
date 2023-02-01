# Returns a preview of the template, used for dashtools UI
import os
import pathlib
from dash import dcc, html, get_app
import plotly.express as px
import pandas as pd


def load_data(data_file: str) -> pd.DataFrame:
    '''
    Load data from /assets directory
    '''
    PATH = pathlib.Path(__file__).parent.resolve()
    return pd.read_csv(PATH.joinpath(data_file))


# Ruh roh.. This may break things. Registering callbacks
# to the main dashboard is not a great idea. Let's refrain
# from doing this. Unfortunately that means no callbacks.

# app=get_app()

# @app.callback(
#     Output("graph", "figure"),
#     Input("button", "n_clicks"))
# def display_graph(n_clicks):
#     # replace with your own data source
#     df = load_data("2014_apple_stock.csv")

#     if n_clicks % 2 == 0:
#         x, y = 'AAPL_x', 'AAPL_y'
#     else:
#         x, y = 'AAPL_y', 'AAPL_x'

#     fig = px.line(df, x=x, y=y)
#     return fig

def render():
    # replace with your own data source
    df = load_data("src/data/2014_apple_stock.csv.template")
    app = get_app()
    # if n_clicks % 2 == 0:
    #     x, y = 'AAPL_x', 'AAPL_y'
    # else:
    #     x, y = 'AAPL_y', 'AAPL_x'

    fig = px.line(df, x='AAPL_x', y='AAPL_y')
    return html.Div([
    html.H4('Simple stock plot from CSV file'),
    # html.Button("Switch Axis", n_clicks=0,
    #             id='button'),
    dcc.Graph(figure=fig),
])