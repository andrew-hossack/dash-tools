from dash import html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dashtools import version


def render() -> html.Div:
    return html.Div(
        [
            html.Div(id='hidden-div'),
            dmc.Center([
                DashIconify(icon='heroicons:command-line-20-solid',
                            height=60, style={'margin-bottom': '8px', 'margin-right': '5px'}),
                html.H2("DashTools", className='dashtools-logo'),
            ], style={"margin-top": "5px",}),
            dmc.Space(h=1, style={'margin-top': '-20px'}),
            html.H6(
                "Application Management Dashboard",
                style={'font-weight': 'inherit', 'font-size': '14px'}
            ),


            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            DashIconify(icon='akar-icons:plus',
                                        style={'margin-right': '5px', 'margin-bottom':'5px'}),
                            "Create"
                        ], href="/create", active="exact"),
                    dbc.NavLink(
                        [
                            DashIconify(icon='akar-icons:cloud',
                                        style={'margin-right': '5px'}),
                            "Deploy"
                        ], href="/deploy", active="exact"),
                    dbc.NavLink(
                        [
                            DashIconify(icon='akar-icons:telescope',
                                        style={'margin-right': '5px'}),
                            "Explore (Preview)"
                        ], href="/explore", active="exact", disabled=True),
                    dbc.NavLink(
                        [
                            DashIconify(icon='akar-icons:question',
                                        style={'margin-right': '5px'}),
                            "Help"
                        ], href="/help", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),

            html.Div([
                html.Hr(style={'width':'200%'}),
                html.Div([
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
                                href="https://pypi.org/project/dash-tools/", target='_blank', style={'text-decoration': 'none', 'color': 'black', 'font-weight': 'lighter'}),
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
                                href="https://dash-tools.readthedocs.io/en/latest/index.html", target='_blank', style={'text-decoration': 'none', 'color': 'black', 'font-weight': 'lighter'}),
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
                                href="https://github.com/andrew-hossack/dash-tools", target='_blank', style={'text-decoration': 'none', 'color': 'black', 'font-weight': 'lighter'}),
                        ]),
                    html.H6(
                        [
                            html.A(
                                [
                                    DashIconify(
                                        icon='material-symbols:bug-report-outline-rounded',
                                        width=20,
                                        style={'margin-right': '8px', 'margin-left': '2px'}),
                                    f'Report Bugs',
                                ],
                                href="https://github.com/andrew-hossack/dash-tools/issues/new/choose", target='_blank', style={'text-decoration': 'none', 'color': 'black', 'font-weight': 'lighter'}),
                        ]),
                ]),
            ], style={'position':'absolute','bottom':'0', 'margin-bottom':'10px'})

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
