"""
DO NOT TOUCH
    This script imports all the test modules available that start with the name test
"""
import os
import unittest
import pkgutil as _pkgutil
from typing import List
from caos._cli_commands import available_commands
from tests.exceptions import MissingCommandsTests

suite: unittest.TestSuite = unittest.TestSuite()
_loader = unittest.TestLoader()
_test_module_names: List[str] = []
_search_path: List[str] = [  # Every path must end with forward slash /
    'tests/caos/cli_commands/',
    'tests/caos/internal/',
    'tests/caos/internal/console/',
    'tests/caos/internal/utils/'
]

_module_info: _pkgutil.ModuleInfo
for _module_info in _pkgutil.iter_modules(path=_search_path):

    if _module_info.name.startswith("test"):
        _test_module_names.append(_module_info.name)
        _full_module_path = _module_info.module_finder.path.replace(os.getcwd() + "/", "")
        _full_module_path = _full_module_path.replace("/", ".") + "." + _module_info.name
        suite.addTests(_loader.loadTestsFromName(_full_module_path))

_expected_command_test_module_names = ["test_" + command for command in available_commands]

_test_module_names_set: set = set(_test_module_names)
_expected_command_test_module_names_set: set = set(_expected_command_test_module_names)
_missing_tests = _expected_command_test_module_names_set.difference(_test_module_names_set)
if _missing_tests:
    _commands = [t.replace("test_", "") for t in _missing_tests]
    raise MissingCommandsTests("There are missing unit tests for the the following commands: {}".format(_commands))
