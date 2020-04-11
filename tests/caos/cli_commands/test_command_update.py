import os
import sys
import shutil
import subprocess
import unittest
from io import StringIO
from caos._cli_commands import command_init, command_update
from caos._internal.console.tools import escape_ansi
from caos._internal.constants import PIP_PATH_VENV_WIN, PIP_PATH_VENV_POSIX, PYTHON_PATH_VENV_WIN, \
    PYTHON_PATH_VENV_POSIX
from caos._internal.utils.os import is_win_os, is_posix_os
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
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)

        if is_win_os():
            self.assertTrue(os.path.isfile(PYTHON_PATH_VENV_WIN))
            self.assertTrue(os.path.isfile(PIP_PATH_VENV_WIN))
            python_path = PYTHON_PATH_VENV_WIN

        elif is_posix_os():
            self.assertTrue(os.path.isfile(PYTHON_PATH_VENV_POSIX))
            self.assertTrue(os.path.isfile(PIP_PATH_VENV_POSIX))
            python_path = PIP_PATH_VENV_POSIX

        self.assertTrue(os.path.isfile(os.path.abspath(_CURRENT_DIR + "/caos.yml")))
        with open(os.path.abspath(_CURRENT_DIR + "/caos.yml"), "w") as file:
            file.write("""
            virtual_environment: "venv"
            dependencies:
                pip: "latest"
                requests: "2.0.0"  
                numpy: "^1.18.2"
                flask: "~1.1.0"            
            """)

        exit_code: int = command_update.entry_point(args=[])
        self.assertEqual(0, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn("INFO: Updating PIP...", messages)
        self.assertIn("SUCCESS: PIP was successfully updated", messages)
        self.assertIn("INFO: Installing dependencies...", messages)
        self.assertIn("SUCCESS: All dependencies have been installed", messages)

        pip_list_process: subprocess.CompletedProcess = subprocess.run(
            [python_path, "-m", "pip", "list"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        if pip_list_process.returncode !=0:
            self.fail("pip list failed")

        output: str = pip_list_process.stdout.lower()
        self.assertIn("pip", output)
        self.assertIn("requests", output)
        self.assertIn("numpy", output)
        self.assertIn("flask", output)


if __name__ == '__main__':
    unittest.main()
