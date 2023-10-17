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
    from dashtools.dashboard.callbacks import (createPage_callbacks,
                                               deployPage_callbacks, router)
    from dashtools.dashboard.components import sidebar
except ModuleNotFoundError:
    from callbacks import createPage_callbacks, deployPage_callbacks, router
    from components import sidebar


app = Dash(
    title="DashTools - Application Dashboard",
    update_title=None,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    assets_folder=Path(__file__).parent.absolute().joinpath('assets'),
    name=__name__,
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"],
)

app.layout = dmc.NotificationsProvider(
    html.Div(
        [
            dmc.Header(id="gh-header", children=[
                dcc.Markdown(
                    '_Thank you for using DashTools!_ If you like it, consider leaving the project a [⭐ on GitHub](https://github.com/andrew-hossack/dash-tools).',
                    link_target="_blank",
                    style={
                        "backgroundColor": "#202020",
                        "color": "white",
                        "text-align": "center",
                        'padding-top':'4px',
                    }, className='padded-bottom')
            ], className='white-link', fixed=True, height=0, ),
            html.Div(id="notifications-container-file-explorer"),
            html.Div(id="notifications-container-file-generator"),
            html.Div(id="notifications-container-app-preview"),
            html.Div(id="notifications-container-app-create"),
            dcc.Location(id="url"),
            sidebar.render(),
            html.Div(
                id="page-content", style={
                    "margin-top": "10px",
                    "margin-left": "22rem",
                    "margin-right": "2rem",
                    "padding": "2rem 1rem",
                    'overflow-x': "hidden",
                }),
        ]))


### Generate necessary callbacks here ###
deployPage_callbacks.generate_callbacks(app)
createPage_callbacks.generate_callbacks(app)
router.generate_callbacks(app)


@contextmanager
def silent_stdout():
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.getLogger(__name__).setLevel(logging.ERROR)
    old_target = sys.stdout
    try:
        with open(os.devnull, "w") as new_target:
            sys.stdout = new_target
            yield new_target
    finally:
        sys.stdout = old_target


def start_dashboard(**args):
    """
    Execute plotly server with only ERROR level logging
    """
    with silent_stdout():
        webbrowser.open('http://127.0.0.1:8050/')
        app.run_server(**args)


if __name__ == "__main__":
    app.run_server(debug=True)
