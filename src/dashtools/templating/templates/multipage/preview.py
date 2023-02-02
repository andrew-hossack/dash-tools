# Returns a preview of the template, used for dashtools UI
from dash import html
import dash_bootstrap_components as dbc

def render():
    navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page)
            for page in ['Page 1', 'Page 2', 'Page 3']
        ],
        nav=True,
        label="More Pages",
    ),
    brand="Multi Page App Plugin Demo",
    color="primary",
    dark=True,
    className="mb-2",
    )

    return dbc.Container(
        [navbar, html.Div([
            html.H2('Multipage App Content'),
            html.A('Dash renders web applications as a "single-page app". When using dcc.Link, the application does not completely reload when navigating, making browsing very fast. Using Dash you can build multi-page apps using dcc.Location and dcc.Link components and callbacks. Dash Pages uses these components and abstracts away the callback logic required for URL routing, making it easy to get up and running with a multi-page app. '),
            html.A(["Learn more about Dash Pages."],href='https://dash.plotly.com/urls')
        ])],
        fluid=True,
    )

