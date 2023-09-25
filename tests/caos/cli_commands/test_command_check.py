import os
import sys
import shutil
import unittest
from io import StringIO
from caos._cli_commands import command_init, command_update, command_check
from caos._internal.console.tools import escape_ansi
from caos._internal.utils.working_directory import get_current_dir

_CURRENT_DIR = get_current_dir()


class TestCommandCheck(unittest.TestCase):
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

    def test_check_command(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)

        self.assertTrue(os.path.isfile(os.path.abspath(_CURRENT_DIR + "/caos.yml")))
        with open(os.path.abspath(_CURRENT_DIR + "/caos.yml"), "w") as file:
            file.write("""
            virtual_environment: "venv"
            dependencies:
                pip: "latest"
                flask: "^2"
                requests: "~2.0.0"
                tensorflow: https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl     
            """)

        exit_code: int = command_update.entry_point(args=[])
        self.assertEqual(0, exit_code)

        exit_code: int = command_check.entry_point(args=[])
        self.assertEqual(0, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn("SUCCESS: All dependencies are installed in the virtual environment", messages)

    def test_check_command_missing_deps(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)

        exit_code: int = command_update.entry_point(args=[])
        self.assertEqual(0, exit_code)

        self.assertTrue(os.path.isfile(os.path.abspath(_CURRENT_DIR + "/caos.yml")))
        with open(os.path.abspath(_CURRENT_DIR + "/caos.yml"), "w") as file:
            file.write("""
            virtual_environment: "venv"
            dependencies:
                pip: "latest"
                requests: "2.0.0"
                tensorflow: https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl     
            """)


        exit_code: int = command_check.entry_point(args=[])
        self.assertEqual(1, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(
            "ERROR: The following dependencies are not installed in the virtual environment:\nrequests\ntensorflow\n", messages
        )

    def test_check_command_installed_versions_dont_match(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)

        self.assertTrue(os.path.isfile(os.path.abspath(_CURRENT_DIR + "/caos.yml")))
        with open(os.path.abspath(_CURRENT_DIR + "/caos.yml"), "w") as file:
            file.write("""
            virtual_environment: "venv"
            dependencies:
                pip: "latest"
                requests: "2.0.0"
                tensorflow: https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl     
            """)

        exit_code: int = command_update.entry_point(args=[])
        self.assertEqual(0, exit_code)

        with open(os.path.abspath(_CURRENT_DIR + "/caos.yml"), "w") as file:
            file.write("""
            virtual_environment: "venv"
            dependencies:
                pip: "19"
                requests: "2.31.0"
                tensorflow: https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-2.0.0-py3-none-any.whl     
            """)

        exit_code: int = command_check.entry_point(args=[])
        self.assertEqual(1, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn(
            "ERROR: The following installed dependencies don't match the versions in the 'caos.yml' file:",
            messages
        )

        self.assertIn("\npip==", messages)
        self.assertIn("\nrequests==2.0.0", messages)
        self.assertIn("\ntensorflow==1.14.0", messages)


if __name__ == '__main__':
    unittest.main()
