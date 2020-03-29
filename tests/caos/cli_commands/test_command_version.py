import sys
import unittest
from io import StringIO
from caos.cli import cli_entry_point, __VERSION__
from caos.style.console.tools import escape_ansi

_VERSION_MESSAGE = "You are using caos version {}".format(__VERSION__)

class TestCommandVersion(unittest.TestCase):
    def setUp(self) -> None:
        self.new_stdout, self.old_stdout = StringIO(), sys.stdout
        self.new_stderr, self.old_stderr = StringIO(), sys.stderr
        sys.stdout, sys.stderr = self.new_stdout, self.new_stderr

    def tearDown(self) -> None:
        sys.stdout, sys.stderr = self.old_stdout, self.old_stderr

    def test_version_full_name(self):
        sys.argv = ["file_name", "--version"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_VERSION_MESSAGE, messages)

    def test_version_short1(self):
        sys.argv = ["file_name", "-v"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_VERSION_MESSAGE, messages)

    def test_version_short2(self):
        sys.argv = ["file_name", "-V"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_VERSION_MESSAGE, messages)


if __name__ == '__main__':
    unittest.main()
