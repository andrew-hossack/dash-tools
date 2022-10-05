from dash import html


def render():
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname x was not recognised..."),
        ]
    )
