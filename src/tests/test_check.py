"""Validate the behaviour of the check module"""

import os
import sys
import shutil
import unittest
import caos.common
import tests.constants
from caos import console
from caos.__main__ import _INIT_COMMAND, _PREPARE_COMMAND, _UPDATE_COMMAND, _CHECK_COMMAND
from caos._internal.check import _console_messages as check_messages

os.chdir(tests.constants._OUT_TEST_FOLDER)


class TestCheck(unittest.TestCase):

    def test_check(self) -> None:
        exists_venv = os.path.isdir(caos.common.constants._CAOS_VENV_DIR)
        if exists_venv:
            shutil.rmtree(path=caos.common.constants._CAOS_VENV_DIR)

        exists_caos_json = os.path.isfile(path=caos.common.constants._CAOS_JSON_FILE)
        if exists_caos_json:
            os.remove(path=caos.common.constants._CAOS_JSON_FILE)

        exists_src = os.path.isdir("./src")
        if exists_src:
            shutil.rmtree(path="./src")
        os.mkdir("./src")

        exists_tests = os.path.isdir("./tests")
        if exists_tests:
            shutil.rmtree(path="./tests")
        os.mkdir("./tests")

        exists_main_py = os.path.isfile("./src/main.py")
        if exists_main_py:
            os.remove(path="./src/main.py")

        with open(file="./src/main.py", mode="w") as main_py:
            main_py.write("print('Hello World')")

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _INIT_COMMAND]
        caos.common.utils.get_func_without_params_stdout(func=console)

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _PREPARE_COMMAND]
        caos.common.utils.get_func_without_params_stdout(func=console)

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _UPDATE_COMMAND]
        caos.common.utils.get_func_without_params_stdout(func=console)

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _CHECK_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console)

        self.assertTrue(check_messages["success"] in out)


if __name__ == '__main__':
    unittest.main()
