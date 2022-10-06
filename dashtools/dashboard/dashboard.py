'''
 # @ Create Time: 2022-10-04 15:30:29.442976
'''

import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, Dash
from dashtools import version
try:
    from . import pages
    from . import callbacks
except ImportError:
    import pages
    import callbacks

app = Dash(
    title="DashTools - Deployment Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True
)


# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


sidebar = html.Div(
    [
        html.Div(id='hidden-div'),
        html.H2("DashTools", className="display-4"),
        html.H5(f'v{version.__version__}', className="display-10"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links",
            className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Deploy", href="/", active="exact"),
                dbc.NavLink("Info", href="/info", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "20rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    },
)

content = html.Div(
    id="page-content", style={
        "margin-left": "22rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    })


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
callbacks.generate_callbacks(app)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return pages.deploy.render()
    elif pathname == "/info":
        return pages.info.render()
    else:
        return pages.error.render()


def start_dashboard(**args):
    # app.logger.setLevel(logging.FATAL) # TODO - Turn off logging
    app.run_server(**args)


if __name__ == "__main__":
    start_dashboard(debug=True)
