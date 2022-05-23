'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 22:09:23
'''
import argparse
import unittest
from dashtools.templating import Templates
from dashtools.templating.buildAppUtils import convert_to_template_or_error, get_template_from_args


class TemplatesTest(unittest.TestCase):

    def test_print_templates(self):
        templates = Templates.Template
        for template in templates:
            # assert keys and values match
            assert template.name.lower() == template.value
            # assert uppercase keys, lowercase values
            assert template.name.upper() == template.name
            assert template.value.lower() == template.value

    def test_convert_to_template_or_error(self):
        # test valid template
        template = convert_to_template_or_error('default')
        assert template == Templates.Template.DEFAULT

        # test invalid template
        with self.assertRaises(SystemExit):
            convert_to_template_or_error('invalid')

    def test_get_template_from_args(self):
        # test no template passed
        args = argparse.Namespace(init=['init'])
        template = get_template_from_args(args)
        assert template == Templates.Template.DEFAULT

        # test template passed
        args = argparse.Namespace(init=['init', 'tabs'])
        template = get_template_from_args(args)
        assert template == 'tabs'
