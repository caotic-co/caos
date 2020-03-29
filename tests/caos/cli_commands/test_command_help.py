import sys
import unittest
from io import StringIO
from caos.cli import cli_entry_point
from caos.style.console.tools import escape_ansi

_DESCRIPTION_MESSAGE = "DESCRIPTION"
_PROGRAM_INFO_MESSAGE = "PROGRAM INFORMATION"
_ARGUMENTS_MESSAGE = "ARGUMENTS"

class TestCommandHelp(unittest.TestCase):
    def setUp(self) -> None:
        self.new_stdout, self.old_stdout = StringIO(), sys.stdout
        self.new_stderr, self.old_stderr = StringIO(), sys.stderr
        sys.stdout, sys.stderr = self.new_stdout, self.new_stderr

    def tearDown(self) -> None:
        sys.stdout, sys.stderr = self.old_stdout, self.old_stderr

    def test_help_full_name(self):
        sys.argv = ["file_name", "--help"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_DESCRIPTION_MESSAGE, messages)
        self.assertIn(_PROGRAM_INFO_MESSAGE, messages)
        self.assertIn(_ARGUMENTS_MESSAGE, messages)

    def test_help_short(self):
        sys.argv = ["file_name", "-h"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_DESCRIPTION_MESSAGE, messages)
        self.assertIn(_PROGRAM_INFO_MESSAGE, messages)
        self.assertIn(_ARGUMENTS_MESSAGE, messages)


if __name__ == '__main__':
    unittest.main()
