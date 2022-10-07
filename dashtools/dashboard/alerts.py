import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify


def render(key: str):
    if key == 'FileNotFoundError':
        return dmc.Notification(
            message="The file path you provided was incorrect. Please check your filepath and try again.",
            title="Warning",
            color='red',
            icon=[DashIconify(icon="ep:warning")],
            action='show',
            id='error-file-not-found'
        )
    elif key == 'PermissionError':
        return dmc.Notification(
            message="You do not have sufficient permission to access that file!",
            title="Warning",
            color='red',
            icon=[DashIconify(icon="ep:warning")],
            action='show',
            id='error-permissions'
        )
