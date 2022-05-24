'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 11:37:09
 # Heroku util functions
'''
import random
import re
import string
import subprocess
from dashtools.data import randomWords
import requests


def heroku_is_installed() -> bool:
    """
    Check that heroku CLI is installed on the system
    Looks for "heroku/X.Y.Z " in the output of "heroku --version"
    """
    regex = r'heroku/[0-9]+\.[0-9]+\.[0-9]+ [a-zA-Z]+'
    isInstalled = True
    try:
        heroku_command_output = subprocess.check_output(
            'heroku --version', shell=True)
        if not re.search(regex, heroku_command_output.decode('utf-8')):
            isInstalled = False
    except subprocess.CalledProcessError:
        isInstalled = False
    return isInstalled


def login_heroku_successful() -> bool:
    """
    Try to log into Heroku
    """
    print(f'dashtools: deploy-heroku: Logging into Heroku...')
    regex = r'Error: quit'
    loginWasSuccessful = True
    try:
        heroku_command_output = subprocess.check_output(
            'heroku login', shell=True)
        if re.search(regex, heroku_command_output.decode('utf-8')):
            loginWasSuccessful = False
    except subprocess.CalledProcessError:
        loginWasSuccessful = False
    return loginWasSuccessful


def check_heroku_app_name_available(heroku_app_name: str) -> bool:
    """
    Check that the app name is available on Heroku

    Returns:
        True if available
        False if not
    """
    try:
        if requests.get(f'https://{heroku_app_name}.herokuapp.com/', headers={'User-Agent': 'Custom'}).status_code == 404:
            return True
    except requests.exceptions.ConnectionError:
        exit('dashtools: deploy-heroku: Invalid Heroku app name')
    return False


def create_app_on_heroku(app_name: str) -> bool:
    """
    Create the project on Heroku and return the git remote URL

    Returns:
        Success of the operation (True/False)
    """
    print(f'dashtools: deploy-heroku: Creating {app_name} on Heroku')
    url_regex = r'https:\/\/git\.heroku\.com\/[a-zA-Z0-9-_]*\.git'
    try:
        heroku_command_output = subprocess.check_output(
            f'heroku create {app_name}', shell=True)
        git_remote_url = re.search(
            url_regex, heroku_command_output.decode('utf-8'))
        try:
            git_remote_url.group(0)
        except AttributeError:
            # No url found. Something is wrong
            return False
    except subprocess.CalledProcessError:
        return False
    return True


def get_heroku_app_name():
    """
    Create or generate app name if one isn't provided
    """
    print('dashtools: deploy-heroku: Please type a unique app name or press enter to generate one automatically.')
    app_name = input('dashtools: App Name (Optional) > ')
    if app_name == '':
        # Generate a random app name with three words
        app_name = '-'.join(randomWords.get_words(3))
        # Append alphanumeric characters to the end of the app name
        app_name += f"-{''.join(random.choices(string.ascii_lowercase + string.digits, k=4))}"
    print(f'dashtools: deploy-heroku: Using app name "{app_name}"')
    return app_name


def validate_heroku_app_name(heroku_app_name) -> bool:
    """
    Heroku app names must start with a letter, end with a
    letter or digit, can only contain lowercase letters,
    numbers, and dashes, and have a minimum length of 3 characters.

    Returns:
        True if valid
        False if invalid
    """
    regex = r'^[a-z][a-z0-9-]{2,}$'
    if re.search(regex, heroku_app_name):
        if heroku_app_name[-1] == '-':
            return False
        return True
    return False
