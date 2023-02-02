# Returns a preview of the template, used for dashtools UI
import pathlib
from dash import dcc, html
import plotly.express as px
import pandas as pd


def load_data(data_file: str) -> pd.DataFrame:
    '''
    Load data from /assets directory
    '''
    PATH = pathlib.Path(__file__).parent.resolve()
    return pd.read_csv(PATH.joinpath(data_file))

def render():
    # replace with your own data source
    df = load_data("src/data/2014_apple_stock.csv.template")
    fig = px.line(df, x='AAPL_x', y='AAPL_y')
    return html.Div([
    html.H4('Simple stock plot from CSV file'),
    dcc.Graph(figure=fig),
])