import os
import sys
import shutil
import unittest
from io import StringIO
from caos._cli_commands import command_run
from caos._internal.constants import CAOS_YAML_FILE_NAME
from caos._internal.console.tools import escape_ansi
from caos._internal.utils.working_directory import get_current_dir

_CURRENT_DIR = get_current_dir()


class TestCommandRun(unittest.TestCase):
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
            os.mkdir("tmp")

    def tearDown(self) -> None:
        self._restore_stdout()

    def test_run_command_hello_world(self):
        yaml_template = """\
        tasks:           
          hello:
            - echo Hello World
        """

        yaml_path: str = os.path.abspath(_CURRENT_DIR + "/" + CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        exit_code: int = command_run.entry_point(args=["hello"])
        self.assertEqual(0, exit_code)

        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn("Hello World", messages)

    def test_run_command_arguments_warning(self):
        yaml_template = """\
        tasks:           
          hello:
            - echo Hello World
        """

        yaml_path: str = os.path.abspath(_CURRENT_DIR + "/" + CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        exit_code: int = command_run.entry_point(args=["hello", "arg"])
        self.assertEqual(0, exit_code)

        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn("WARNING: The tasks can't receive arguments", messages)

    def test_run_command_unknown_task(self):
        yaml_template = """\
        tasks:           
          hello:
            - echo Hello World
        """

        yaml_path: str = os.path.abspath(_CURRENT_DIR + "/" + CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        with self.assertRaises(Exception) as context:
            command_run.entry_point(args=["bye"])
        self.assertIn("No task named 'bye' was found", str(context.exception))

    def test_run_command_non_zero_exit(self):
        yaml_template = """\
        tasks:           
          hello:
            - exit 1
        """

        yaml_path: str = os.path.abspath(_CURRENT_DIR + "/" + CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        with self.assertRaises(Exception) as context:
            command_run.entry_point(args=["hello"])

        self.assertIn("Within the task 'hello' the step 'exit 1' returned a non zero exit code", str(context.exception))

    def test_run_command_recursion(self):
        yaml_template = """\
        tasks:           
          1:
            - echo 1
          2:
            - 1
            - echo 2
          3:
            - 2
            - echo 3
        """

        yaml_path: str = os.path.abspath(_CURRENT_DIR + "/" + CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        exit_code: int = command_run.entry_point(args=["3"])
        self.assertEqual(0, exit_code)

        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn("1\n2\n3", messages)

    def test_run_command_recursion_exceeded(self):
        yaml_template = """\
        tasks:           
          1:
            - 1
            - echo 1
        """

        yaml_path: str = os.path.abspath(_CURRENT_DIR + "/" + CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        with self.assertRaises(RecursionError) as context:
            command_run.entry_point(args=["1"])

        self.assertIn("Maximum recursion depth exceeded", str(context.exception))




if __name__ == '__main__':
    unittest.main()
