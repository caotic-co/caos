"""Validate the behaviour of the init module"""

import os
import sys
import unittest
import common
from src.caos import console
from src.caos._internal.init import _console_messages
from src.caos._internal.templates.caos_json import example_template
from common import utils, constants

class TestInit(unittest.TestCase):

    def test_create_json(self) -> None:
        os.chdir(constants._OUT_TEST)

        exists = os.path.isfile(path='./caos.json')
        if exists:
            os.remove(path='./caos.json')

        sys.argv = [sys.argv[0], "init"]
        out = utils.get_func_without_params_stdout(func=console) 

        self.assertEqual(out, _console_messages["success"])

        exists = os.path.isfile(path='./caos.json')
        if exists:
            with open(file='./caos.json' , mode='r') as caos_json_file:
                self.assertEqual(
                    caos_json_file.read(),
                    example_template
                )
    
    def test_existing_json(self) -> None:
        os.chdir(constants._OUT_TEST)

        exists = os.path.isfile(path='./caos.json')
        if not exists:
            with open(file='./caos.json', mode='w') as fake_file:
                fake_file.write("")        

        sys.argv = [sys.argv[0], "init"]
        out = utils.get_func_without_params_stdout(func=console) 

        self.assertEqual(out, _console_messages["file_exists"])



if __name__ == '__main__':
    unittest.main()




