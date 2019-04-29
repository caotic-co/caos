"""Validate the behaviour of the init module"""

import os
import sys
import unittest
import tests.constants
from src.caos import console
from src.caos.__main__ import _INIT_COMMAND
from src.caos._internal.init import _console_messages
from src.caos._internal.templates.caos_json import example_template

os.chdir(tests.constants._OUT_TEST_FOLDER)
import common #Import common only after changing folder





class TestInit(unittest.TestCase):

    def test_create_json(self) -> None:
        exists = os.path.isfile(path=common.constants._CAOS_JSON_FILE)
        if exists:
            os.remove(path=common.constants._CAOS_JSON_FILE)

        sys.argv = [sys.argv[0], _INIT_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console) 

        self.assertEqual(out, _console_messages["success"])

        exists = os.path.isfile(path=common.constants._CAOS_JSON_FILE)
        if exists:
            with open(file=common.constants._CAOS_JSON_FILE , mode='r') as caos_json_file:
                self.assertEqual(
                    caos_json_file.read(),
                    example_template
                )
    
    def test_existing_json(self) -> None:
        exists = os.path.isfile(path=common.constants._CAOS_JSON_FILE)
        if not exists:
            with open(file=common.constants._CAOS_JSON_FILE, mode='w') as fake_file:
                fake_file.write("")        

        sys.argv = [sys.argv[0], _INIT_COMMAND]
        out = common.utils.get_func_without_params_stdout(func=console) 

        self.assertEqual(out, _console_messages["file_exists"])

if __name__ == '__main__':
    unittest.main()
