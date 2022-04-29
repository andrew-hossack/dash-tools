'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 22:09:23
'''
import unittest
from dash_tools.deploy import herokuUtils


class HerokuUtilsTest(unittest.TestCase):

    def test_validate_heroku_app_name(self):
        # test valid app name
        assert herokuUtils.validate_heroku_app_name('valid-app-name') is True

        # test invalid app name
        assert herokuUtils.validate_heroku_app_name(
            '1invalid-app-name') is False
        assert herokuUtils.validate_heroku_app_name(
            'fo') is False
        assert herokuUtils.validate_heroku_app_name(
            'HELLO') is False
        assert herokuUtils.validate_heroku_app_name(
            'invalid-app-name-') is False
