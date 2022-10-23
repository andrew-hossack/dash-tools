'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 23:09:06
'''
import configparser
import unittest
try:
    from dashtools.data import configUtils
except ModuleNotFoundError:
    from ..dashtools.data import configUtils


class ConfigUtilsTest(unittest.TestCase):

    def test_get_config_smoketest(self):
        config = configUtils._get_config()
        self.assertIsInstance(config, configparser.ConfigParser)

    def test_get_config_value(self):
        try:
            # python_shell_cmd should is set with the pypi package
            configUtils.get_config_value('python_shell_cmd')
        except KeyError:
            self.fail('KeyError')

    def test_set_config_value(self):
        # TODO
        assert True
