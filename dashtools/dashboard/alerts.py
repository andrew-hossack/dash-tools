import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

# NOTIFICATION_DURATION_SECONDS = 8


def render(key: str):
    if key == 'FileNotFoundError':
        return dmc.Notification(
            message="The file path you provided does not exist. Please check your filepath and try again.",
            title="Warning",
            color='red',
            icon=[DashIconify(icon="ep:warning")],
            action='show',
            # autoClose=NOTIFICATION_DURATION_SECONDS,
            id='error-file-not-found'
        )
    elif key == 'PermissionError':
        return dmc.Notification(
            message="You do not have sufficient permission to access that file!",
            title="Warning",
            color='red',
            icon=[DashIconify(icon="ep:warning")],
            action='show',
            # autoClose=NOTIFICATION_DURATION_SECONDS,
            id='error-permissions'
        )
    elif key == 'FileRequiredError':
        return dmc.Notification(
            message="You must have an Open File in File Explorer to do this action!",
            title="Warning",
            color='red',
            icon=[DashIconify(icon="ep:warning")],
            action='show',
            # autoClose=NOTIFICATION_DURATION_SECONDS,
            id='error-permissions'
        )
    elif key == 'NameRequiredError':
        return dmc.Notification(
            message="A Render App Name is needed to do this action!",
            title="Warning",
            color='red',
            icon=[DashIconify(icon="ep:warning")],
            action='show',
            # autoClose=NOTIFICATION_DURATION_SECONDS,
            id='error-permissions'
        )
