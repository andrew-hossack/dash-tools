'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-04-28 23:09:06
'''
import unittest
from dashtools.data import randomWords


class RandomWordsTest(unittest.TestCase):
    """
    Tests RandomWords for generating heroku name
    """

    def test_random_words(self):
        # Test words are random
        words = randomWords.get_words(10)
        self.assertEqual(len(words), 10)
        new_words = randomWords.get_words(10)
        self.assertNotEqual(words, new_words)
