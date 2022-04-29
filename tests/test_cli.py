'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 22:09:23
'''
import unittest
from unittest.mock import MagicMock

from dash_tools.cli import cli
from dash_tools.deploy import deployHeroku
from dash_tools.templating import buildTemplate, templateUtils


class CLITest(unittest.TestCase):

    def test_handle_args_deploy_heroku(self):
        args = MagicMock()
        args.init = None
        args.templates = False
        args.deploy_heroku = 'test'
        args.parse_args = MagicMock(return_value=args)
        deployHeroku.deploy_app_to_heroku = MagicMock()
        cli.handle_args(args)
        assert deployHeroku.deploy_app_to_heroku.called

    def test_handle_args_init(self):
        args = MagicMock()
        args.init = ['test']
        args.templates = False
        args.deploy_heroku = None
        args.parse_args = MagicMock(return_value=args)
        buildTemplate.create_app = MagicMock()
        cli.handle_args(args)
        assert buildTemplate.create_app.called

    def test_handle_args_templates(self):
        args = MagicMock()
        args.init = None
        args.templates = True
        args.deploy_heroku = None
        args.parse_args = MagicMock(return_value=args)
        templateUtils.print_templates = MagicMock()
        cli.handle_args(args)
        assert templateUtils.print_templates.called

    def test_print_help(self):
        args = MagicMock()
        args.init = None
        args.templates = False
        args.deploy_heroku = None
        args.parse_args = MagicMock(return_value=args)
        args.print_help = MagicMock()
        with self.assertRaises(SystemExit):
            cli.handle_args(args)
