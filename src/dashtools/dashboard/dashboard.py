'''
 # @ Create Time: 2022-10-04 15:30:29.442976
'''
import logging
import os
import sys
import webbrowser
from contextlib import contextmanager
from pathlib import Path

import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, dcc, html

try:
    from callbacks import createPage_callbacks, deployPage_callbacks, router
    from components import sidebar
except ModuleNotFoundError:
    from . import createPage_callbacks, deployPage_callbacks
    from .callbacks import createPage_callbacks, deployPage_callbacks, router
    from .components import sidebar

app = Dash(
    title="DashTools - Application Management Dashboard",
    update_title=None,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    assets_folder=Path(__file__).parent.absolute().joinpath('assets'),
    name=__name__
)

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

content = html.Div(
    id="page-content", style={
        "margin-left": "22rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    })

app.layout = dmc.NotificationsProvider(
    html.Div(
        [
            html.Div(id="notifications-container-file-explorer"),
            html.Div(id="notifications-container-file-generator"),
            dcc.Location(id="url"),
            sidebar.render(),
            content
        ]))

deployPage_callbacks.generate_callbacks(app)
createPage_callbacks.generate_callbacks(app)
router.generate_callbacks(app)


def start_dashboard(**args):
    """
    Execute plotly server with only ERROR level logging
    """

    @contextmanager
    def silence_stdout():
        old_target = sys.stdout
        try:
            with open(os.devnull, "w") as new_target:
                sys.stdout = new_target
                yield new_target
        finally:
            sys.stdout = old_target

    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.getLogger(__name__).setLevel(logging.ERROR)

    with silence_stdout():
        webbrowser.open('http://127.0.0.1:8050/')
        app.run_server(**args)


if __name__ == "__main__":
    app.run_server(debug=True)
