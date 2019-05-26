"""Validate the behaviour of the run module"""

import os
import sys
import shutil
import unittest
import caos.common
import tests.constants
import tests.templates
from caos import console
from caos.__main__ import _INIT_COMMAND, _PREPARE_COMMAND, _UPDATE_COMMAND, _TEST_COMMAND
from caos.__main__ import _console_messages as console_messages
from caos._internal.test import _console_messages as test_messages

os.chdir(tests.constants._OUT_TEST_FOLDER)


class TestTest(unittest.TestCase):    

    def test_test(self) -> None:           
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
        
        test_py = os.path.isfile("./tests/test.py")
        if test_py:
            os.remove(path="./tests/test.py")

        with open(file="./tests/test.py", mode="w") as test_py:            
            test_py.write(tests.templates.python_unit_test_file)       
               
        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _INIT_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console)

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _PREPARE_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console)
        
        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _UPDATE_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console)
         
        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _TEST_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console)

        self.assertTrue("OK" in out)
        self.assertFalse("FAILED (failures=" in out)


if __name__ == '__main__':
    unittest.main()
