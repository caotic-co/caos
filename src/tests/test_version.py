"""Validate the behaviour of the of the console commands related with the version"""

import sys
import unittest
import caos.common.utils
from caos import console
from caos.__main__ import _console_messages


class TestVersion(unittest.TestCase):

    def test_version_command(self) -> None:
        sys.argv = [sys.argv[0], "--version"]
        out = caos.common.utils.get_func_without_params_stdout(func=console) 
        self.assertEqual(out, _console_messages["version"])

        sys.argv = [sys.argv[0], "-v"]
        out = caos.common.utils.get_func_without_params_stdout(func=console)
        self.assertEqual(out, _console_messages["version"])


if __name__ == '__main__':
    unittest.main()