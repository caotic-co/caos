import re
from caos._internal.constants import ValidDependencyVersionRegex
from caos._internal.exceptions import InvalidDependencyVersionFormat, UnexpectedError
from typing import NewType

PipReadyDependency = NewType(name="PipReadyDependency", tp=str)


def get_dependency_version_format(dependency_name: str, version: str) -> ValidDependencyVersionRegex:
    """
    Raises:
        InvalidDependencyVersionFormat
    """
    if re.match(pattern=ValidDependencyVersionRegex.MAJOR_MINOR_PATCH.value, string=version):
        return ValidDependencyVersionRegex.MAJOR_MINOR_PATCH

    if re.match(pattern=ValidDependencyVersionRegex.MAJOR_MINOR.value, string=version):
        return ValidDependencyVersionRegex.MAJOR_MINOR

    if re.match(pattern=ValidDependencyVersionRegex.MAJOR.value, string=version):
        return ValidDependencyVersionRegex.MAJOR

    if re.match(pattern=ValidDependencyVersionRegex.LATEST.value, string=version):
        return ValidDependencyVersionRegex.LATEST

    if re.match(pattern=ValidDependencyVersionRegex.WHL.value, string=version):
        return ValidDependencyVersionRegex.WHL

    raise InvalidDependencyVersionFormat(
        "Invalid version format for the dependency '{dep}'. Only the following formats are allowed: 'latest', "
        "'/path/to/file.whl' and dependencies with a 'final release' format (see "
        "https://www.python.org/dev/peps/pep-0440/#final-releases)"
        .format(dep=dependency_name)
    )


def generate_pip_ready_dependency(dependency_name: str, version: str) -> PipReadyDependency:
    """
    Raises:
        InvalidDependencyVersionFormat
        UnexpectedError
    """
    dependency_regex: ValidDependencyVersionRegex = get_dependency_version_format(
        dependency_name=dependency_name,
        version=version
    )

    if dependency_regex == ValidDependencyVersionRegex.MAJOR_MINOR_PATCH:  # (^|~) X.X.X
        if version.startswith("~"):  # Allow patch updates
            return version  # ~X.X.X

        elif version.startswith("^"):  # Allow minor updates
            version = version.replace("^", "")
            major, minor, patch = version.split(".")
            return "~{}.{}".format(major, minor)  # ~X.X

        else:  # Allow exact version
            return "=={}".format(version)  # ==X.X.X

    elif dependency_regex == ValidDependencyVersionRegex.MAJOR_MINOR:
        if version.startswith("~"):  # Allow patch updates
            version = version.replace("~", "")
            major, minor = version.split(".")
            return "~{}.{}.0".format(major, minor)  # ~X.X.0

        elif version.startswith("^"):  # Allow minor updates
            version = version.replace("^", "~")
            return version  # ~X.X

        else:  # Allow exact version
            return "=={}".format(version)  # ==X.X

    elif dependency_regex == ValidDependencyVersionRegex.MAJOR:
        if version.startswith("~"):  # Allow patch updates
            version = version.replace("~", "")
            return "~{}.0.0".format(version)  # ~X.0.0

        elif version.startswith("^"):  # Allow minor updates
            version = version.replace("^", "")
            return "~{}.0".format(version)  # ~X.0

        else:  # Allow exact version
            return "=={}".format(version)  # ==X

    elif dependency_regex == ValidDependencyVersionRegex.LATEST:
        return dependency_name

    elif dependency_regex == ValidDependencyVersionRegex.WHL:
        return version

    raise UnexpectedError("The dependency given should have thrown 'InvalidDependencyVersionFormat' but it did not")
