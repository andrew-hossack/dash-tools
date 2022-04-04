'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-03 17:51:36
 # Uses heroku CLI to deploy to Heroku.
'''

import os


def deploy_to_heroku(invoke_directory: os.PathLike):
    """
    Uses the heroku CLI to deploy the current project to Heroku
    """
    print(invoke_directory)
