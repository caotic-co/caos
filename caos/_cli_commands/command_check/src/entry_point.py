import os
import re
import sys

import subprocess
from io import StringIO
from typing import List
from caos._internal.types import ExitCode
from caos._internal.utils.yaml import get_virtual_environment_from_yaml
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._internal.constants import (
    CAOS_YAML_FILE_NAME, DEFAULT_VIRTUAL_ENVIRONMENT_NAME,
    PIP_PATH_VENV_WIN, PIP_PATH_VENV_POSIX
)
from caos._cli_commands.raise_exceptions import (
    raise_missing_yaml_exception,
    raise_missing_virtual_environment_exception,
    raise_missing_pip_binary_exception
)


wheel_file_regex = re.compile(
    r"""^(?P<namever>(?P<name>.+?)-(?P<ver>.*?))
    ((-(?P<build>\d[^-]*?))?-(?P<pyver>.+?)-(?P<abi>.+?)-(?P<plat>.+?)
    \.whl|\.dist-info)$""",
    re.VERBOSE
)


def main(args: List[str]) -> ExitCode:
    current_dir: str = get_current_dir()
    if not os.path.isfile(os.path.abspath(current_dir + "/" + CAOS_YAML_FILE_NAME)):
        raise_missing_yaml_exception()

    venv_name: str = get_virtual_environment_from_yaml()

    if not os.path.isdir(os.path.abspath(current_dir + "/" + venv_name)):
        raise_missing_virtual_environment_exception(env_name=venv_name)

    if is_win_os():
        pip_path: str = PIP_PATH_VENV_WIN.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)
    elif is_posix_os():
        pip_path: str = PIP_PATH_VENV_POSIX.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)

    if not os.path.isfile(pip_path):
        raise_missing_pip_binary_exception(env_name=venv_name)



    return ExitCode(0)
