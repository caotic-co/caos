import sys
import unittest
from io import StringIO
from caos._cli import cli_entry_point
from caos._internal.console.tools import escape_ansi

_NO_ARG_MESSAGE = "No argument given, if you need help try typing 'caos --help'"
_UNKNOWN_ARG = "Unknown argument, if you need help try typing 'caos --help'"


class TestInvalidArguments(unittest.TestCase):
    def _redirect_stdout(self):
        self.new_stdout, self.old_stdout = StringIO(), sys.stdout
        self.new_stderr, self.old_stderr = StringIO(), sys.stderr
        sys.stdout, sys.stderr = self.new_stdout, self.new_stderr

    def _restore_stdout(self):
        sys.stdout, sys.stderr = self.old_stdout, self.old_stderr

    def setUp(self) -> None:
        self._redirect_stdout()

    def tearDown(self) -> None:
        self._restore_stdout()

    def test_invalid_command_argument_unknown(self):
        sys.argv = ["file_name", "some_weird_invalid_argument"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_UNKNOWN_ARG, messages)

    def test_invalid_command_argument_missing(self):
        sys.argv = ["file_name"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_NO_ARG_MESSAGE, messages)


if __name__ == '__main__':
    unittest.main()
