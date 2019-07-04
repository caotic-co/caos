"""Validate the behaviour of the run module"""

import os
import sys
import shutil
import subprocess
import unittest
import caos.common
import tests.constants
from caos import console
from caos.__main__ import _PREPARE_COMMAND, _PYTHON_COMMAND

os.chdir(tests.constants._OUT_TEST_FOLDER)


class TestPython(unittest.TestCase):

    def test_run(self) -> None:           
        exists_venv = os.path.isdir("./venv")
        if exists_venv:
            shutil.rmtree(path="./venv")

        exists_src = os.path.isdir("./src")
        if exists_src:
            shutil.rmtree(path="./src")
        os.mkdir("./src")

        exists_main_py = os.path.isfile("./src/main.py")
        if exists_main_py:
            os.remove(path="./src/main.py")

        with open(file="./src/main.py", mode="w") as main_py:            
            main_py.write("print('Hello World')")

        sys.argv = [caos.common.constants._UNIT_TEST_SUITE_NAME, _PREPARE_COMMAND]
        out = caos.common.utils.get_func_without_params_stdout(func=console)

        result = subprocess.check_output(
            args=[sys.executable, "-c", "from caos import console; console()", _PYTHON_COMMAND, "-c", "print('Python run test')"],
            cwd="../../"
        ).decode("utf-8")

        self.assertTrue('Python run test' in result)


if __name__ == '__main__':
    unittest.main()
