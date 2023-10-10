import os
import sys
import shutil
import unittest
from io import StringIO
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._cli_commands import command_init
from caos._cli_commands import command_run
from caos._internal.constants import CAOS_YAML_FILE_NAME
from caos._internal.console.tools import escape_ansi
from caos._internal.utils.working_directory import get_current_dir

_CURRENT_TESTS_DIR = get_current_dir()
_PROJECT_DIR = os.path.abspath(os.getcwd())


class TestCommandRun(unittest.TestCase):
    def _redirect_stdout(self):
        self.new_stdout, self.old_stdout = StringIO(), sys.stdout
        self.new_stderr, self.old_stderr = StringIO(), sys.stderr
        sys.stdout, sys.stderr = self.new_stdout, self.new_stderr

    def _restore_stdout(self):
        sys.stdout, sys.stderr = self.old_stdout, self.old_stderr

    def setUp(self) -> None:
        self._redirect_stdout()
        os.chdir(_PROJECT_DIR)
        if os.path.isdir("tmp"):
            shutil.rmtree("tmp")
            os.mkdir("tmp")
        os.chdir(_CURRENT_TESTS_DIR)

    def tearDown(self) -> None:
        self._restore_stdout()
        os.chdir(_PROJECT_DIR)

    def test_run_command_hello_world(self):
        yaml_template = """\
        tasks:           
          hello:
            - echo Hello World
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
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

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
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

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
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

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        with self.assertRaises(Exception) as context:
            command_run.entry_point(args=["hello"])

        self.assertIn("Within the task 'hello' the step 'exit 1' returned a non zero exit code", str(context.exception))

    def test_run_multi_line_command_successful(self):
        yaml_template = """\
        tasks:           
          true_task_posix:
            - |
              if true &> /dev/null; then
                echo [TRUE]
              else
                echo [FALSE]
                exit 1
              fi
          
          true_task_windows:
            - |
              if 1 equ 1(
                echo [TRUE]
              ) else (
                echo [FALSE]
                exit 1
              )
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        if is_posix_os():
            exit_code: int = command_run.entry_point(args=["true_task_posix"])
            self.assertEqual(0, exit_code)
        if is_win_os():
            exit_code: int = command_run.entry_point(args=["true_task_windows"])
            self.assertEqual(0, exit_code)

        messages: str = escape_ansi(self.new_stdout.getvalue())
        self.assertIn("[TRUE]", messages)

    def test_run_multi_line_command_failure(self):
        yaml_template = """\
        tasks:                          
          false_task_posix:
            - |
              if false &> /dev/null; then
                echo [TRUE]
              else
                echo [FALSE]
                exit 1
              fi
          
          false_task_windows:
            - |
              if 1 equ 2(
                echo [TRUE]
              ) else (
                echo [FALSE]
                exit 1
              )        
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        self._restore_stdout()
        if is_posix_os():
            with self.assertRaises(Exception) as context:
                command_run.entry_point(args=["false_task_posix"])
            self.assertIn("Within the task 'false_task_posix' the step", str(context.exception))
            self.assertIn("returned a non zero exit code", str(context.exception))

        if is_win_os():
            with self.assertRaises(Exception) as context:
                command_run.entry_point(args=["false_task_windows"])
            self.assertIn("Within the task 'false_task_windows' the step", str(context.exception))
            self.assertIn("returned a non zero exit code", str(context.exception))

        messages: str = escape_ansi(self.new_stdout.getvalue())
        self.assertIn("[FALSE]", messages)


    def test_run_incomplete_command_failure(self):
        yaml_template = """\
        virtual_environment: venv
        
        tasks:                          
          incomplete_task:
            - |
              caos pip install        
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        exit_code: int = command_init.entry_point(args=[""])
        self.assertEqual(0, exit_code)

        with self.assertRaises(Exception) as context:
            command_run.entry_point(args=["incomplete_task"])

        messages: str = escape_ansi(self.new_stdout.getvalue())
        self.assertIn("Within the task 'incomplete_task' the step", str(context.exception))
        self.assertIn("returned a non zero exit code", str(context.exception))

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

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        exit_code: int = command_run.entry_point(args=["3"])
        self.assertEqual(0, exit_code)

        messages: str = escape_ansi(self.new_stdout.getvalue())

        if is_posix_os():
            self.assertIn("1\n\n2\n\n3\n\n", messages)
        elif is_win_os():
            self.assertIn("1 \n\n2 \n\n3 \n\n", messages)

    def test_run_command_recursion_exceeded(self):
        yaml_template = """\
        tasks:           
          1:
            - 1
            - echo 1
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        with self.assertRaises(RecursionError) as context:
            command_run.entry_point(args=["1"])

        self.assertIn("Maximum recursion depth exceeded", str(context.exception))

    def test_run_command_keep_declared_env_vars_in_the_same_task(self):

        yaml_template = """\
        tasks:           
          posix:
            - export MY_VAR='Hello World Var'
            - echo $MY_VAR
            
          windows:
            - set MY_VAR='Hello World Var'
            - echo %MY_VAR%
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        exit_code: int = 1
        if is_posix_os():
            exit_code = command_run.entry_point(args=["posix"])
        elif is_win_os():
            exit_code = command_run.entry_point(args=["windows"])

        self.assertEqual(0, exit_code)

        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn("Hello World Var", messages)

    def test_run_command_keep_declared_env_vars_in_nested_tasks(self):

        yaml_template = """\
        tasks:
          posix_parent:
            - export MY_VAR='Hello World Var'
            - posix
                       
          posix:
            - echo $MY_VAR

          windows_parent:
            - set MY_VAR='Hello World Var'
            - windows
                     
          windows:
            - echo %MY_VAR%
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        exit_code: int = 1
        if is_posix_os():
            exit_code = command_run.entry_point(args=["posix_parent"])
        elif is_win_os():
            exit_code = command_run.entry_point(args=["windows_parent"])

        self.assertEqual(0, exit_code)

        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertIn("Hello World Var", messages)

    def test_run_command_keep_cwd_in_the_same_task(self):

        yaml_template = """\
        tasks:           
          posix:
            - cd folder1
            - cd sub_folder1
            - pwd

          windows:
            - cd folder1
            - cd sub_folder1
            - dir
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        os.mkdir("folder1")
        os.mkdir("folder1/sub_folder1")
        self.assertTrue(os.path.isdir("folder1"))
        self.assertTrue(os.path.isdir("folder1/sub_folder1"))

        exit_code: int = 1
        if is_posix_os():
            exit_code = command_run.entry_point(args=["posix"])
            messages: str = escape_ansi(self.new_stdout.getvalue())
            self.assertEqual(0, exit_code)
            self.assertIn("folder1/sub_folder1", messages)
        elif is_win_os():
            exit_code = command_run.entry_point(args=["windows"])
            messages: str = escape_ansi(self.new_stdout.getvalue())
            self.assertEqual(0, exit_code)
            self.assertIn("folder1\\sub_folder1", messages)

    def test_run_command_keep_cwd_in_nested_tasks(self):

        yaml_template = """\
        tasks:
          posix_parent:
            - cd folder2
            - cd sub_folder2
            - posix

          posix:
            - pwd

          windows_parent:
            - cd folder2
            - cd sub_folder2
            - windows

          windows:
            - dir
        """

        yaml_path: str = os.path.abspath(CAOS_YAML_FILE_NAME)
        self.assertFalse(os.path.isfile(yaml_path))
        with open(file=yaml_path, mode="w") as yaml_file:
            yaml_file.write(yaml_template)

        self.assertTrue(os.path.isfile(yaml_path))

        os.mkdir("folder2")
        os.mkdir("folder2/sub_folder2")
        self.assertTrue(os.path.isdir("folder2"))
        self.assertTrue(os.path.isdir("folder2/sub_folder2"))

        exit_code: int = 1
        if is_posix_os():
            exit_code = command_run.entry_point(args=["posix_parent"])
            self.assertEqual(0, exit_code)
            messages: str = escape_ansi(self.new_stdout.getvalue())
            self.assertIn("folder2/sub_folder2", messages)

        elif is_win_os():
            exit_code = command_run.entry_point(args=["windows_parent"])
            self.assertEqual(0, exit_code)
            messages: str = escape_ansi(self.new_stdout.getvalue())
            self.assertIn("folder2\\sub_folder2", messages)


if __name__ == '__main__':
    unittest.main()
