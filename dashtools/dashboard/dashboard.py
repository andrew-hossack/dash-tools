'''
 # @ Create Time: 2022-10-04 15:30:29.442976
'''
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, Input, Output, dcc, html
from dash_iconify import DashIconify
from dashtools import version
try:
    import callbacks
    from pages import createPage, deployPage, errorPage, infoPage
except ModuleNotFoundError:
    from . import callbacks
    from .pages import createPage, deployPage, errorPage, infoPage

app = Dash(
    title="DashTools - Development Dashboard",
    update_title=None,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)


# Declare server for Heroku deployment. Needed for Procfile.
server = app.server


sidebar = html.Div(
    [
        html.Div(id='hidden-div'),
        html.H2("DashTools",  style={'weight': 'bold', 'font-size': '50px'}),
        html.H6(
            [
                html.A(
                    [
                        DashIconify(
                            icon='logos:pypi',
                            width=20,
                            style={'margin-right': '10px'}),
                        f'PyPi v{version.__version__}',
                    ],
                    href="https://pypi.org/project/dash-tools/", target='_blank', style={'text-decoration': 'none', 'color': 'black'}),
            ]),
        html.H6(
            [
                html.A(
                    [
                        DashIconify(
                            icon='file-icons:readthedocs',
                            width=15,
                            style={'margin-right': '10px', 'margin-left': '5px'}),
                        f'Read the Docs',
                    ],
                    href="https://dash-tools.readthedocs.io/en/latest/index.html", target='_blank', style={'text-decoration': 'none', 'color': 'black'}),
            ]),
        html.H6(
            [
                html.A(
                    [
                        DashIconify(
                            icon='ant-design:github-filled',
                            width=20,
                            style={'margin-right': '8px', 'margin-left': '2px'}),
                        f'GitHub',
                    ],
                    href="https://github.com/andrew-hossack/dash-tools", target='_blank', style={'text-decoration': 'none', 'color': 'black'}),
            ]),
        html.Hr(),
        html.H6(
            "Plotly Dash Application Dashboard",
            className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Create", href="/create", active="exact"),
                dbc.NavLink("Deploy", href="/deploy", active="exact"),
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


app.layout = dmc.NotificationsProvider(
    html.Div(
        [
            html.Div(id="notifications-container"),
            dcc.Location(id="url"),
            sidebar,
            content
        ]))

callbacks.generate_callbacks(app)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    # Clear data
    if pathname == "/deploy" or pathname == '/':
        deployPage.terminal.clear()
        return deployPage.render()
    elif pathname == "/info":
        return infoPage.render()
    elif pathname == "/create":
        return createPage.render()
    else:
        return errorPage.render()


def start_dashboard(**args):
    # app.logger.setLevel(logging.FATAL) # TODO - Turn off logging
    app.run_server(**args)


if __name__ == "__main__":
    start_dashboard(debug=True)
