'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-08-11 18:25:19
 '''
import unittest
from dashtools.version import __version__ as dashtools_version
from docs.source.version import __version__ as docs_version


class VersionoMatch(unittest.TestCase):

    def test_version_match(self):
        """
        Version in docs/source/version.py must match dashtools/version.py version!
        """
        self.assertEqual(docs_version, dashtools_version)
