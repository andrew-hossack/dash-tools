import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify


def render():
    return html.Div(
        [
            dmc.Center([
                DashIconify(icon='emojione:hammer-and-wrench',
                            width=35, color='light-gray', style={'margin-right': '20px'}),
                dmc.Title(["Under Construction"], order=1),
                DashIconify(icon='emojione:hammer-and-wrench',
                            width=35, color='light-gray', style={'margin-left': '20px'})
            ], style={'margin-top':'30px'}),
            html.Div([
                dmc.Text([""]),
                dcc.Markdown(
                    'Developers wanted! Please check out [https://github.com/andrew-hossack/dash-tools/pull/102](https://github.com/andrew-hossack/dash-tools/pull/102) for more details.',
                    link_target="_blank",
                    style={
                        "color": "black",
                        "text-align": "center",
                    })
                    ],
            ),
            dmc.Center([
                dmc.Image(
                    src='https://cdn.thenewstack.io/media/2022/06/2baa04d0-help-wanted-sign.jpg', alt='Help Wanted',
                    width=800,
                    radius=10,
                    withPlaceholder=True,
                    placeholder=[dmc.Loader(color="gray", size="sm")])
            ]),
        ],
        style={"height": "90vh", "padding": "10px"}
    )
