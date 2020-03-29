"""
DO NOT TOUCH
    This script imports all the test modules available that start with the name test
"""
import unittest
import pkgutil as _pkgutil
from typing import List
from caos.cli_commands import available_commands
from tests.exceptions import MissingCommandsTests

suite: unittest.TestSuite = unittest.TestSuite()
_loader = unittest.TestLoader()
_test_module_names: List[str] = []
_search_path: List[str] = ['tests/caos/cli_commands/', 'tests/caos/other_tests']

_module_info: _pkgutil.ModuleInfo
for _module_info in _pkgutil.iter_modules(path=_search_path):

    if _module_info.name.startswith("test"):
        _test_module_names.append(_module_info.name)
        suite.addTests(_loader.loadTestsFromName("tests.caos.cli_commands.{}".format(_module_info.name)))

_expected_command_test_module_names = ["test_" + command for command in available_commands]

_test_module_names_set: set = set(_test_module_names)
_expected_command_test_module_names_set: set = set(_expected_command_test_module_names)
if not _test_module_names_set.issubset(_expected_command_test_module_names_set):
    raise MissingCommandsTests(
        "There are missing unit tests for the the following commands: {}"
        .format(_expected_command_test_module_names_set.difference(_test_module_names_set))
    )
