"""Validate the behaviour of the prepare module"""

import os
import sys
import shutil
import unittest
import tests.constants
from caos import console
from caos.__main__ import _PREPARE_COMMAND
from caos._internal.prepare import _console_messages

os.chdir(tests.constants._OUT_TEST_FOLDER)
import common #Import common only after changing folder

class TestInit(unittest.TestCase):

    def test_create_env(self) -> None:     
        exists = os.path.isdir(common.constants._CAOS_VENV_DIR)
        if exists:
            shutil.rmtree(path=common.constants._CAOS_VENV_DIR)

        sys.argv = [sys.argv[0], _PREPARE_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console) 

        self.assertEqual(out, _console_messages["success"])

    def test_create_env_with_existing_folder(self) -> None:
        exists = os.path.isdir(common.constants._CAOS_VENV_DIR)
        if not exists:
            os.mkdir(path=common.constants._CAOS_VENV_DIR)

        sys.argv = [sys.argv[0], _PREPARE_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console) 

        self.assertEqual(out, _console_messages["venv_exists"])

if __name__ == '__main__':
    unittest.main()
