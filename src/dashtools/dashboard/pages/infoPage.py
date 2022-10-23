import dash_mantine_components as dmc
from dash import html, dcc


def render():
    return html.Div(
        [
            dmc.Header(
                [
                    html.H3("About")
                ], height=50,),
            # dmc.Divider(variant="dotted", style={
            #     'margin-left': '60px', 'margin-right': '60px'}),
            dmc.Stack(
                [
                    html.Div(
                        dcc.Link(
                            'GitHub', href='https://github.com/andrew-hossack/dash-tools')
                    ),
                    html.Div(
                        dcc.Link(
                            'Foo', href='https://github.com/andrew-hossack/dash-tools')
                    ),
                    html.Div(
                        dcc.Link(
                            'Foo', href='https://github.com/andrew-hossack/dash-tools')
                    ),
                ]
            )

        ]
    )
