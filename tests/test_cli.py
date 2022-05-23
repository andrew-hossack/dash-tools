'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 22:09:23
'''
import unittest
from unittest.mock import MagicMock

from dash_tools.cli import cli
from dash_tools.deploy import deployHeroku
from dash_tools.templating import buildApp, buildAppUtils


class CLITest(unittest.TestCase):
    """
    TODO Need to update for new CLI
    """

    # def test_main_deploy_heroku(self):
    #     args = MagicMock()
    #     args.init = None
    #     args.templates = False
    #     args.deploy_heroku = 'test'
    #     args.parse_args = MagicMock(return_value=args)
    #     deployHeroku.deploy_app_to_heroku = MagicMock()
    #     cli.main(args)
    #     assert deployHeroku.deploy_app_to_heroku.called

    # def test_main_init(self):
    #     args = MagicMock()
    #     args.init = ['test']
    #     args.templates = False
    #     args.deploy_heroku = None
    #     args.parse_args = MagicMock(return_value=args)
    #     buildApp.create_app = MagicMock()
    #     cli.main(args)
    #     assert buildApp.create_app.called

    # def test_main_templates(self):
    #     args = MagicMock()
    #     args.init = None
    #     args.templates = True
    #     args.deploy_heroku = None
    #     args.parse_args = MagicMock(return_value=args)
    #     buildAppUtils.print_templates = MagicMock()
    #     cli.main(args)
    #     assert buildAppUtils.print_templates.called

    # def test_print_help(self):
    #     args = MagicMock()
    #     args.init = None
    #     args.templates = False
    #     args.deploy_heroku = None
    #     args.parse_args = MagicMock(return_value=args)
    #     args.print_help = MagicMock()
    #     with self.assertRaises(SystemExit):
    #         cli.main(args)
