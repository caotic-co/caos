import os
import sys
import shutil
import unittest
from io import StringIO
from caos._cli_commands import command_init, command_update
from caos._internal.console.tools import escape_ansi
from caos._internal.utils.working_directory import get_current_dir

_CURRENT_DIR = get_current_dir()


class TestCommandUpdate(unittest.TestCase):
    def _redirect_stdout(self):
        self.new_stdout, self.old_stdout = StringIO(), sys.stdout
        self.new_stderr, self.old_stderr = StringIO(), sys.stderr
        sys.stdout, sys.stderr = self.new_stdout, self.new_stderr

    def _restore_stdout(self):
        sys.stdout, sys.stderr = self.old_stdout, self.old_stderr

    def setUp(self) -> None:
        self._redirect_stdout()
        if os.path.isdir("tmp"):
            shutil.rmtree("tmp")

    def tearDown(self) -> None:
        self._restore_stdout()

    def test_update_command(self):
        pass


if __name__ == '__main__':
    unittest.main()
