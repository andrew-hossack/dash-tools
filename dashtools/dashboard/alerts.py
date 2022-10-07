import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def render():
    return dmc.Notification(
        message="The file path you provided was incorrect. Please check your filepath and try again.",
        title="Warning",
        color='red',
        icon=[DashIconify(icon="ep:warning")],
        action='show',
        id='file-explorer-alert'
    )
