# Returns a preview of the template, used for dashtools UI
from dash import html, dcc
import dash_leaflet as dl
import pandas as pd
import numpy as np


def render():
    lats = [56, 56, 56]
    lons = [10, 11, 12]
    df = pd.DataFrame(columns=["lat", "lon"], data=np.column_stack((lats, lons)))
    # Create markers from data frame.
    markers = [dl.Marker(position=[row["lat"], row["lon"]])
            for i, row in df.iterrows()]
    tiles = [dl.TileLayer(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"), dl.LayerGroup(markers)]
    return html.Div([
        html.H1(children='Dash Leaflet App'),

        html.Div(children='''
            Dash: A web application framework for your data.
        '''),

        html.Hr(),

        dl.Map(children=tiles,
            style={'width': "100%", 'height': "100%"}, center=[56, 11], zoom=9, id="map"),

        dcc.Markdown(
            "Learn more about [Dash Leaflet](https://github.com/thedirtyfew/dash-leaflet)")
    ], style={'width': '1000px', 'height': '500px'})