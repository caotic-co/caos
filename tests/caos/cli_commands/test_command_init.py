import os
import sys
import shutil
import unittest
from io import StringIO
from caos._cli_commands import command_init
from caos._internal.console.tools import escape_ansi
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.constants import (
    PYTHON_PATH_VENV_POSIX,
    PYTHON_PATH_VENV_WIN,
    PIP_PATH_VENV_POSIX,
    PIP_PATH_VENV_WIN
)

_CURRENT_DIR = get_current_dir()
_CAOS_PROMPT = "[caos] init --> "
_CREATING_VIRTUAL_ENVIRONMENT_MESSAGE = _CAOS_PROMPT + "INFO: Creating a new virtual environment..."
_VIRTUAL_ENVIRONMENT_CREATED_MESSAGE = _CAOS_PROMPT + "SUCCESS: A new virtual environment was created"
_VIRTUAL_ENVIRONMENT_EXISTS_MESSAGE = _CAOS_PROMPT + "INFO: The virtual environment already exists so "\
                                      "a new one won't be created"
_CREATING_YAML_MESSAGE = _CAOS_PROMPT + "INFO: Creating 'caos.yml'..."
_YAML_CREATED_MESSAGE = _CAOS_PROMPT + "SUCCESS: 'caos.yml' created"
_YAML_EXISTS_MESSAGE = _CAOS_PROMPT + "INFO: The 'caos.yml' file already exists"
_OVERRIDE_YAML_ERROR_MESSAGE = _CAOS_PROMPT + "ERROR: <<OverrideYamlConfigurationException>> "\
                               "To use a different virtual environment edit the respective key within the 'caos.yml' "\
                               "file and then execute 'caos init'"
_MISSING_PIP_WARNING_MESSAGE = _CAOS_PROMPT + "WARNING: The virtual environment does not have a 'pip' binary"
_MISSING_PYTHON_ERRROR_MESSAGE = _CAOS_PROMPT + "ERROR: <<MissingBinaryException>> The virtual environment "\
                                "does not have a 'python' binary"


class TestCommandInit(unittest.TestCase):

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

    def test_init_command_no_args(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertTrue(os.path.isdir(os.path.abspath(_CURRENT_DIR+"/venv")))
        self.assertTrue(os.path.isfile(os.path.abspath(_CURRENT_DIR+"/caos.yml")))

        self.assertIn(_CREATING_VIRTUAL_ENVIRONMENT_MESSAGE, messages)
        messages: str = messages.replace(_CREATING_VIRTUAL_ENVIRONMENT_MESSAGE, "", 1)

        self.assertIn(_VIRTUAL_ENVIRONMENT_CREATED_MESSAGE, messages)
        messages: str = messages.replace(_VIRTUAL_ENVIRONMENT_CREATED_MESSAGE, "", 1)

        self.assertIn(_CREATING_YAML_MESSAGE, messages)
        messages: str = messages.replace(_CREATING_YAML_MESSAGE, "", 1)

        self.assertIn(_YAML_CREATED_MESSAGE, messages)

    def test_init_command_my_env(self):
        exit_code: int = command_init.entry_point(args=["my_env"])
        self.assertEqual(0, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertTrue(os.path.isdir(os.path.abspath(_CURRENT_DIR+"/my_env")))
        self.assertTrue(os.path.isfile(os.path.abspath(_CURRENT_DIR+"/caos.yml")))

        self.assertIn(_CREATING_VIRTUAL_ENVIRONMENT_MESSAGE, messages)
        messages: str = messages.replace(_CREATING_VIRTUAL_ENVIRONMENT_MESSAGE, "", 1)

        self.assertIn(_VIRTUAL_ENVIRONMENT_CREATED_MESSAGE, messages)
        messages: str = messages.replace(_VIRTUAL_ENVIRONMENT_CREATED_MESSAGE, "", 1)

        self.assertIn(_CREATING_YAML_MESSAGE, messages)
        messages: str = messages.replace(_CREATING_YAML_MESSAGE, "", 1)

        self.assertIn(_YAML_CREATED_MESSAGE, messages)

    def test_init_command_venv_twice(self):
        command_init.entry_point(args=[])
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())

        self.assertTrue(os.path.isdir(os.path.abspath(_CURRENT_DIR+"/venv")))
        self.assertTrue(os.path.isfile(os.path.abspath(_CURRENT_DIR+"/caos.yml")))
        
        self.assertIn(_CREATING_VIRTUAL_ENVIRONMENT_MESSAGE, messages)
        messages: str = messages.replace(_CREATING_VIRTUAL_ENVIRONMENT_MESSAGE, "", 1)
        
        self.assertIn(_VIRTUAL_ENVIRONMENT_CREATED_MESSAGE, messages)
        messages: str = messages.replace(_VIRTUAL_ENVIRONMENT_CREATED_MESSAGE, "", 1)
        
        self.assertIn(_CREATING_YAML_MESSAGE, messages)
        messages: str = messages.replace(_CREATING_YAML_MESSAGE, "", 1)
        
        self.assertIn(_YAML_CREATED_MESSAGE, messages)
        messages: str = messages.replace(_YAML_CREATED_MESSAGE, "", 1)
        
        self.assertIn(_VIRTUAL_ENVIRONMENT_EXISTS_MESSAGE, messages)
        messages: str = messages.replace(_VIRTUAL_ENVIRONMENT_EXISTS_MESSAGE, "", 1)
        
        self.assertIn(_YAML_EXISTS_MESSAGE, messages)

    def test_init_command_existing_yaml(self):
        command_init.entry_point(args=[])
        exit_code: int = command_init.entry_point(args=["my_env"])
        self.assertEqual(1, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())
        self.assertTrue(os.path.isdir(os.path.abspath(_CURRENT_DIR+"/venv")))
        self.assertTrue(os.path.isfile(os.path.abspath(_CURRENT_DIR+"/caos.yml")))
        self.assertIn(_OVERRIDE_YAML_ERROR_MESSAGE, messages)

    def test_init_command_venv_binaries(self):
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(0, exit_code)
        if is_win_os():
            self.assertTrue(os.path.isfile(PYTHON_PATH_VENV_WIN))
            self.assertTrue(os.path.isfile(PIP_PATH_VENV_WIN))
            os.remove(PYTHON_PATH_VENV_WIN)
            os.remove(PIP_PATH_VENV_WIN)

        elif is_posix_os():
            self.assertTrue(os.path.isfile(PYTHON_PATH_VENV_POSIX))
            self.assertTrue(os.path.isfile(PIP_PATH_VENV_POSIX))
            os.remove(PYTHON_PATH_VENV_POSIX)
            os.remove(PIP_PATH_VENV_POSIX)

        self._restore_stdout()
        self._redirect_stdout()
        exit_code: int = command_init.entry_point(args=[])
        self.assertEqual(1, exit_code)
        messages: str = escape_ansi(self.new_stdout.getvalue())
        self.assertIn(_YAML_EXISTS_MESSAGE, messages)
        self.assertIn(_VIRTUAL_ENVIRONMENT_EXISTS_MESSAGE, messages)
        self.assertIn(_MISSING_PIP_WARNING_MESSAGE, messages)
        self.assertIn(_MISSING_PYTHON_ERRROR_MESSAGE, messages)


if __name__ == '__main__':
    unittest.main()