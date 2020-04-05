import os
import sys
import shutil
from io import StringIO
import unittest
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.yaml import get_virtual_environment_from_yaml, get_dependencies_from_yaml


class TestYamlUtil(unittest.TestCase):
    def setUp(self) -> None:
        self.new_stdout, self.old_stdout = StringIO(), sys.stdout
        self.new_stderr, self.old_stderr = StringIO(), sys.stderr
        sys.stdout, sys.stderr = self.new_stdout, self.new_stderr
        if os.path.isdir("tmp"):
            shutil.rmtree("tmp")

    def tearDown(self) -> None:
        sys.stdout, sys.stderr = self.old_stdout, self.old_stderr

    def test_get_virtual_environment_from_yaml_default(self):
        test_caos_yaml = "virtual_environment: 'venv'"
        with open(file=os.path.abspath(get_current_dir() + "/" + "caos.yml"), mode="w") as file:
            file.write(test_caos_yaml)

        self.assertEqual("venv", get_virtual_environment_from_yaml())

    def test_get_virtual_environment_from_yaml_custom(self):
        test_caos_yaml = "virtual_environment: 'custom_venv'"
        with open(file=os.path.abspath(get_current_dir() + "/" + "caos.yml"), mode="w") as file:
            file.write(test_caos_yaml)

        self.assertEqual("custom_venv", get_virtual_environment_from_yaml())

    def test_get_dependencies_from_yaml(self):
        test_caos_yaml = """\
        dependencies:
            dep1: "latest"
            dep2: ^1.5.0
            dep3: ~2
            dep4: ./file.whl
        """
        with open(file=os.path.abspath(get_current_dir()+"/"+"caos.yml"), mode="w") as file:
            file.write(test_caos_yaml)

        dependencies = get_dependencies_from_yaml()
        expected_result = {
            "dep1": "dep1",
            "dep2": "~1.5",
            "dep3": "~2.0.0",
            "dep4": "./file.whl"
        }
        self.assertEqual(expected_result, dependencies)


if __name__ == '__main__':
    unittest.main()
