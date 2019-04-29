"""Validate the behaviour of the prepare module"""

import os
import sys
import shutil
import unittest
import tests.constants
from src.caos import console
from src.caos.__main__ import _INIT_COMMAND, _PREPARE_COMMAND, _UPDATE_COMMAND
from src.caos._internal.update import _console_messages

os.chdir(tests.constants._OUT_TEST_FOLDER)
import common #Import common only after changing folder

class TestInit(unittest.TestCase):

    def test_update(self) -> None:   
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
            main_py.write("")

        sys.argv = [sys.argv[0], _INIT_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console)

        sys.argv = [sys.argv[0], _PREPARE_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console)
        
        sys.argv = [sys.argv[0], _UPDATE_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console) 

        self.assertEqual(out, _console_messages["downloading"]+"\n"+_console_messages["success"])

if __name__ == '__main__':
    unittest.main()
