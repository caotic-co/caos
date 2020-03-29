import sys
import unittest
from io import StringIO
from caos.cli import cli_entry_point
from caos.style.console.tools import escape_ansi

_NO_ARG_MESSAGE = "No argument given, if you need help try typing 'caos --help'"
_UNKNOWN_ARG = "Unknown argument, if you need help try typing 'caos --help'"

class TestInvalidArguments(unittest.TestCase):
    def setUp(self) -> None:
        self.new_stdout, self.old_stdout = StringIO(), sys.stdout
        self.new_stderr, self.old_stderr = StringIO(), sys.stderr
        sys.stdout, sys.stderr = self.new_stdout, self.new_stderr

    def tearDown(self) -> None:
        sys.stdout, sys.stderr = self.old_stdout, self.old_stderr

    def test_unknown_argument(self):
        sys.argv = ["file_name", "some_weird_invalid_argument"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_UNKNOWN_ARG, messages)

    def test_no_argument(self):
        sys.argv = ["file_name"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_NO_ARG_MESSAGE, messages)


if __name__ == '__main__':
    unittest.main()
