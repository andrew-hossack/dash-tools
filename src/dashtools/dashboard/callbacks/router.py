'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-10-23 14:52:57
'''

from dash import Dash, Input, Output, dcc

try:
    from dashtools.dashboard.pages import createPage, deployPage, errorPage, infoPage
except ModuleNotFoundError:
    from dashtools.dashboard.pages import createPage, deployPage, errorPage, infoPage


def generate_callbacks(app: Dash):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == '/':
            # Setup url redirect to default page
            return dcc.Location(id="url", pathname='/deploy')
        elif pathname == "/deploy":
            deployPage.terminal.clear()
            return deployPage.render()
        elif pathname == "/info":
            return infoPage.render()
        elif pathname == "/create":
            createPage.terminal.clear()
            return createPage.render()
        else:
            return errorPage.render()
