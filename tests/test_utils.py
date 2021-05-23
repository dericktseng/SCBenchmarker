import unittest
import sys
import os

# sys.path hack to correctly import files
dir_path = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(dir_path, '..'))
sys.path.append(project_root)

from src import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.testdict = dict()
        self.assertFalse('test' in self.testdict)

    def test_add_if_key_exists_init(self):
        """ Tests only adding one value """
        utils.add_if_key_exists(self.testdict, 'test', 3)
        self.assertEqual(self.testdict['test'], 3)

    def test_add_if_key_exists_add(self):
        """ Tests adding two same values. """
        # tests adding value to key
        utils.add_if_key_exists(self.testdict, 'test', 3)
        self.assertEqual(self.testdict['test'], 3)

        # adds secondary value to key
        utils.add_if_key_exists(self.testdict, 'test', 5)
        self.assertEqual(self.testdict['test'], 8)


if __name__ == '__main__':
    unittest.main()
