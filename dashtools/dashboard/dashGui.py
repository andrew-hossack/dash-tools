'''
 # @ Create Time: 2022-10-04 15:30:29.442976
'''

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

app = Dash(__name__, title="DashTools - Deployment Dashboard")


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


def start_dashboard():
    # app.logger.setLevel(logging.FATAL) # TODO - Turn off logging
    app.run_server()
