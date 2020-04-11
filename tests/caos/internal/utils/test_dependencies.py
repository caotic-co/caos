import unittest

from caos._internal.exceptions import InvalidDependencyVersionFormat
from caos._internal.utils.dependencies import generate_pip_ready_dependency


class TestDependenciesUtil(unittest.TestCase):

    def test_dependency_util_generate_pip_ready_dependency(self):
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="1.1.1"), "==1.1.1")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="2.2"), "==2.2")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="3"), "==3")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="^4.4.4"), "~=4.4")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="^5.5"), "~=5.5")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="^6"), "~=6.0")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="~7.7.7"), "~=7.7.7")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="~8.8"), "~=8.8.0")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="~9"), "~=9.0.0")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="LATEST"), "test")
        self.assertEqual(generate_pip_ready_dependency(dependency_name="test", version="latest"), "test")
        self.assertEqual(
            generate_pip_ready_dependency(
                dependency_name="test",
                version="./test-1.0.0-py3-none-any.whl"),
            "./test-1.0.0-py3-none-any.whl"
        )
        self.assertEqual(
            generate_pip_ready_dependency(
                dependency_name="test",
                version="./test-1.0.0-py3-none-any.dist-info"),
            "./test-1.0.0-py3-none-any.dist-info"
        )

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="a.b.c")
            self.assertIn("Invalid version format for the dependency", context.exception)

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="1.2.")
            self.assertIn("Invalid version format for the dependency", context.exception)

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="1.a.3")
            self.assertIn("Invalid version format for the dependency", context.exception)

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="==1.2.3")
            self.assertIn("Invalid version format for the dependency", context.exception)

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="^1.2.3.1")
            self.assertIn("Invalid version format for the dependency", context.exception)

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="~1.2.3.1")
            self.assertIn("Invalid version format for the dependency", context.exception)

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="1.2.3.4")
            self.assertIn("Invalid version format for the dependency", context.exception)

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="./test.whl")
            self.assertIn("The version format for the wheel dependency 'test' is invalid", context.exception)

        with self.assertRaises(InvalidDependencyVersionFormat) as context:
            generate_pip_ready_dependency(dependency_name="test", version="./test.dist-info")
            self.assertIn("The version format for the wheel dependency 'test' is invalid", context.exception)


if __name__ == '__main__':
    unittest.main()
