import os
import sys
import shutil
import unittest
from io import StringIO
from caos._cli_commands import command_init, command_pip
from caos._internal.console.tools import escape_ansi
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.constants import DEFAULT_VIRTUAL_ENVIRONMENT_NAME, PIP_PATH_VENV_POSIX, PIP_PATH_VENV_WIN

_CURRENT_DIR = get_current_dir()
_MISSING_PIP_BINARY_MESSAGE = "The virtual environment does not have a 'pip' binary. "\
                              "Try deleting the folder 'venv' and run 'caos init'"
_MISSING_VIRTUAL_ENVIRONMENT_MESSAGE = "No virtual environment 'venv' could be found. Try running first 'caos init'"


class TestCommandPip(unittest.TestCase):
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

    def test_pip_command_list(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)
        self._restore_stdout()
        self._redirect_stdout()

        exit_code: int = command_pip.entry_point(args=["list"])
        self.assertEqual(0, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn("pip", messages)
        self.assertIn("setuptools", messages)

    def test_pip_command_error(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)
        exit_code: int = command_pip.entry_point(args=["random_unknown_command_1234"])
        self.assertEqual(1, exit_code)

    def test_pip_command_missing_binary(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)

        if is_win_os():
            self.assertTrue(os.path.isfile(PIP_PATH_VENV_WIN))
            os.remove(PIP_PATH_VENV_WIN)

        elif is_posix_os():
            self.assertTrue(os.path.isfile(PIP_PATH_VENV_POSIX))
            os.remove(PIP_PATH_VENV_POSIX)

        with self.assertRaises(Exception) as context:
            command_pip.entry_point(args=["search", "caos"])
        self.assertIn(_MISSING_PIP_BINARY_MESSAGE, str(context.exception))

    def test_pip_command_virtual_environment(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)

        venv_path: str = os.path.abspath(_CURRENT_DIR + "/" + DEFAULT_VIRTUAL_ENVIRONMENT_NAME)
        self.assertTrue(os.path.isdir(venv_path))
        shutil.rmtree(venv_path)

        with self.assertRaises(Exception) as context:
            command_pip.entry_point(args=["help", "install)"])
        self.assertIn(_MISSING_VIRTUAL_ENVIRONMENT_MESSAGE, str(context.exception))


if __name__ == '__main__':
    unittest.main()
