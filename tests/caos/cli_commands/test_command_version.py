import sys
import unittest
from io import StringIO
from caos import __VERSION__
from caos._cli import cli_entry_point
from caos._internal.console.tools import escape_ansi

_VERSION_MESSAGE = "You are using caos version {}".format(__VERSION__)


class TestCommandVersion(unittest.TestCase):
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

    def test_version_command(self):
        sys.argv = ["file_name", "--version"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_VERSION_MESSAGE, messages)

    def test_version_command_alias1(self):
        sys.argv = ["file_name", "-v"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_VERSION_MESSAGE, messages)

    def test_version_command_alias2(self):
        sys.argv = ["file_name", "-V"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_VERSION_MESSAGE, messages)


if __name__ == '__main__':
    unittest.main()
