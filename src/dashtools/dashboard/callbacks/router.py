'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-10-23 14:52:57
'''

from dash import Dash, Input, Output, dcc

from dashtools.dashboard.pages import explorePage

from ..pages import explorePage

try:
    from dashtools.dashboard.pages import createPage, deployPage, helpPage
except ModuleNotFoundError:
    from ..pages import createPage, deployPage, helpPage


def generate_callbacks(app: Dash):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == '/':
            # Setup url redirect to default page
            return dcc.Location(id="url", pathname='/create')
        elif pathname == "/deploy":
            return deployPage.render()
        elif pathname == "/explore":
            return explorePage.render()
        elif pathname == "/create":
            return createPage.render()
        elif pathname == "/help":
            return helpPage.render()
        else:
            # Can also implement custom error page here
            return dcc.Location(id="url", pathname='/')
