"""Validate the behaviour of the run module"""

import os
import sys
import shutil
import unittest
import common 
import tests.constants
from caos import console
from caos.__main__ import _INIT_COMMAND, _PREPARE_COMMAND, _UPDATE_COMMAND, _RUN_COMMAND
from caos.__main__ import _console_messages as console_messages
from caos._internal.run import _console_messages as run_messages

os.chdir(tests.constants._OUT_TEST_FOLDER)


class TestRun(unittest.TestCase):
    

    def test_run(self) -> None:
           
        exists_venv = os.path.isdir(common.constants._CAOS_VENV_DIR)
        if exists_venv:
            shutil.rmtree(path=common.constants._CAOS_VENV_DIR)
        
        exists_caos_json = os.path.isfile(path=common.constants._CAOS_JSON_FILE)
        if exists_caos_json:
            os.remove(path=common.constants._CAOS_JSON_FILE)

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
       
        sys.argv = [common.constants._UNIT_TEST_SUITE_NAME, _INIT_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console)

        sys.argv = [common.constants._UNIT_TEST_SUITE_NAME, _PREPARE_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console)
        
        sys.argv = [common.constants._UNIT_TEST_SUITE_NAME, _UPDATE_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console)
         
        sys.argv = [common.constants._UNIT_TEST_SUITE_NAME, _RUN_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console)

        self.assertTrue("Hello World" in out)

        


if __name__ == '__main__':
    unittest.main()
