"""Validate the behaviour of the of the console commands related with the help"""

import sys
import unittest
import common.utils

from src.caos import console
from src.caos.__main__ import _console_messages

class TestInit(unittest.TestCase):

    def test_help_command(self) -> None:
        sys.argv = [sys.argv[0], "help"]
        out = common.utils.get_func_without_params_stdout(func=console) 
        self.assertEqual(out, _console_messages["help"])
    
    def test_help_suggestion(self) -> None:
        sys.argv = [sys.argv[0], "fake_argument"]
        out = common.utils.get_func_without_params_stdout(func=console) 
        self.assertEqual(out, _console_messages["need_help"])


if __name__ == '__main__':
    unittest.main()

