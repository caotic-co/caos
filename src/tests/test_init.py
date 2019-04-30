"""Validate the behaviour of the init module"""

import os
import sys
import unittest
import caos.common
import tests.constants
from caos import console
from caos.__main__ import _INIT_COMMAND
from caos._internal.init import _console_messages
from caos._internal.templates.caos_json import example_template

os.chdir(tests.constants._OUT_TEST_FOLDER)

class TestInit(unittest.TestCase):

    def test_create_json(self) -> None:
        exists = os.path.isfile(path=caos.common.constants._CAOS_JSON_FILE)
        if exists:
            os.remove(path=caos.common.constants._CAOS_JSON_FILE)

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _INIT_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console) 

        self.assertTrue(_console_messages["success"] in out)

        exists = os.path.isfile(path=caos.common.constants._CAOS_JSON_FILE)
        if exists:
            with open(file=caos.common.constants._CAOS_JSON_FILE , mode='r') as caos_json_file:
                self.assertEqual(
                    caos_json_file.read(),
                    example_template
                )
    
    def test_existing_json(self) -> None:
        exists = os.path.isfile(path=caos.common.constants._CAOS_JSON_FILE)
        if not exists:
            with open(file=caos.common.constants._CAOS_JSON_FILE, mode='w') as fake_file:
                fake_file.write("")        

        sys.argv = [sys.argv[0], _INIT_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console) 

        self.assertTrue(_console_messages["file_exists"] in out)

if __name__ == '__main__':
    unittest.main()
