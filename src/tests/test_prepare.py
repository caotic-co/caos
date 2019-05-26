"""Validate the behaviour of the prepare module"""

import os
import sys
import shutil
import unittest
import caos.common
import tests.constants
from caos import console
from caos.__main__ import _PREPARE_COMMAND
from caos._internal.prepare import _console_messages as prepare_messages

os.chdir(tests.constants._OUT_TEST_FOLDER)


class TestPrepare(unittest.TestCase):

    def test_create_env(self) -> None:     
        exists = os.path.isdir(caos.common.constants._CAOS_VENV_DIR)
        if exists:
            shutil.rmtree(path=caos.common.constants._CAOS_VENV_DIR)

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _PREPARE_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console) 

        self.assertTrue(prepare_messages["success"] in out)

    def test_create_env_with_existing_folder(self) -> None:
        exists = os.path.isdir(caos.common.constants._CAOS_VENV_DIR)
        if not exists:
            os.mkdir(path=caos.common.constants._CAOS_VENV_DIR)

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _PREPARE_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console) 

        self.assertTrue(prepare_messages["venv_exists"] in out)


if __name__ == '__main__':
    unittest.main()
