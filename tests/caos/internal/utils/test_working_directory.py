import unittest
from caos._internal.utils.working_directory import is_dev_environment, get_current_dir


class TestWorkingDirectoryUtil(unittest.TestCase):

    def test_working_directory_util_current_directory(self):
        self.assertTrue(is_dev_environment())
        self.assertIn("tmp", get_current_dir())


if __name__ == '__main__':
    unittest.main()
