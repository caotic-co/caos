import sys
import unittest
from io import StringIO
from caos._cli import cli_entry_point
from caos._internal.console.tools import escape_ansi

_DESCRIPTION_MESSAGE = "DESCRIPTION"
_DESCRIPTION_CONTENT_MESSAGE = "A simple dependency management tool and tasks executor for Python projects"
_PROGRAM_INFO_MESSAGE = "PROGRAM INFORMATION"
_HELP_COMMAND_ARGUMENTS_MESSAGE = "--help or -h"
_HELP_COMMAND_DESCRIPTION_MESSAGE = "Shows documentation about the available arguments and its usage"
_VERSION_COMMAND_ARGUMENTS_MESSAGE = "--version, -v or -V"
_VERSION_COMMAND_DESCRIPTION_MESSAGE = "Shows the currently installed version"

_ARGUMENTS_MESSAGE = "ARGUMENTS"

class TestCommandHelp(unittest.TestCase):

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

    def test_help_command(self):
        sys.argv = ["file_name", "--help"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_DESCRIPTION_MESSAGE, messages)
        self.assertIn(_DESCRIPTION_CONTENT_MESSAGE, messages)

        self.assertIn(_PROGRAM_INFO_MESSAGE, messages)
        self.assertIn(_HELP_COMMAND_ARGUMENTS_MESSAGE, messages)
        self.assertIn(_HELP_COMMAND_DESCRIPTION_MESSAGE, messages)
        self.assertIn(_VERSION_COMMAND_ARGUMENTS_MESSAGE, messages)
        self.assertIn(_VERSION_COMMAND_DESCRIPTION_MESSAGE, messages)

        self.assertIn(_ARGUMENTS_MESSAGE, messages)

    def test_help_command_alias(self):
        sys.argv = ["file_name", "-h"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(_DESCRIPTION_MESSAGE, messages)
        self.assertIn(_DESCRIPTION_CONTENT_MESSAGE, messages)

        self.assertIn(_PROGRAM_INFO_MESSAGE, messages)
        self.assertIn(_HELP_COMMAND_ARGUMENTS_MESSAGE, messages)
        self.assertIn(_HELP_COMMAND_DESCRIPTION_MESSAGE, messages)
        self.assertIn(_VERSION_COMMAND_ARGUMENTS_MESSAGE, messages)
        self.assertIn(_VERSION_COMMAND_DESCRIPTION_MESSAGE, messages)

        self.assertIn(_ARGUMENTS_MESSAGE, messages)

    def test_help_command_init_output(self):
        sys.argv = ["file_name", "-h"]
        cli_entry_point()
        messages: str = escape_ansi(self.new_stdout.getvalue())
        self.assertIn("Creates a Python virtual environment based on the configuration", messages)
        self.assertIn("of an existing 'caos.yml' file in the current directory.", messages)
        self.assertIn("If the 'caos.yml' file is not present in the current directory a", messages)
        self.assertIn("new virtual environment and configuration file are created.", messages)
        self.assertIn("caos init", messages)
        self.assertIn("caos init [VIRTUAL_ENV_NAME]", messages)


if __name__ == '__main__':
    unittest.main()
