import os
import sys
import subprocess
from typing import List, NewType
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.yaml import get_virtual_environment_from_yaml
from caos._internal.utils.os import is_supported_os, is_posix_os, is_win_os
from caos._internal.console import caos_command_print, INFO_MESSAGE, WARNING_MESSAGE, SUCCESS_MESSAGE, ERROR_MESSAGE
from caos._internal.exceptions import UnsupportedOS, MissingBinaryException
from caos._internal.constants import (
    CAOS_YAML_FILE_NAME, PYTHON_PATH_VENV_WIN, PYTHON_PATH_VENV_POSIX, PIP_PATH_VENV_WIN, PIP_PATH_VENV_POSIX
)
from .exceptions import CreateVirtualEnvironmentException, OverrideYamlConfigurationException
from .constants import (
    NAME, _DEFAULT_VIRTUAL_ENVIRONMENT_NAME, _CAOS_YAML_TEMPLATE
)

ExitCode = NewType("ExitCode", int)


def create_caos_yaml(current_dir: str, env_name: str):
    """
    Raises:
        OpenCaosFileException
        InvalidCaosFileFormat
        WrongKeyTypeInYamlFile
        OverrideYamlConfigurationException
    """
    caos_yml_path: str = os.path.abspath(current_dir + "/" + CAOS_YAML_FILE_NAME);
    if os.path.isfile(caos_yml_path):
        env_name_in_yaml = get_virtual_environment_from_yaml()

        if env_name and env_name != env_name_in_yaml:
            raise OverrideYamlConfigurationException(
                "To use a different virtual environment edit the respective key within the '{CAOS_YAML}' file "
                "and then execute 'caos init' "
                    .format(CAOS_YAML=CAOS_YAML_FILE_NAME)
            )

        caos_command_print(
            command=NAME,
            message=INFO_MESSAGE("The '{CAOS_YAML}' file already exists".format(CAOS_YAML=CAOS_YAML_FILE_NAME))
        )
        return

    caos_command_print(command=NAME, message=INFO_MESSAGE("Creating '{CAOS_YAML}'...").format(CAOS_YAML=CAOS_YAML_FILE_NAME))

    if not env_name:
        env_name = _DEFAULT_VIRTUAL_ENVIRONMENT_NAME

    with open(file=caos_yml_path, mode="w") as caos_yml_file:
        caos_yml_file.write(
            _CAOS_YAML_TEMPLATE.format(VENV_NAME=env_name)
        )

    caos_command_print(
        command=NAME,
        message=SUCCESS_MESSAGE("'{CAOS_YAML}' created".format(CAOS_YAML=CAOS_YAML_FILE_NAME))
    )
    return


def create_virtual_env(current_dir:str):
    """
    Raises:
        OpenCaosFileException
        InvalidCaosFileFormat
        WrongKeyTypeInYamlFile
        CreateVirtualEnvironmentException
        MissingBinaryException
    """
    env_name = get_virtual_environment_from_yaml()
    env_path : str = os.path.abspath(current_dir + "/" + env_name);
    if os.path.isdir(env_path):
        caos_command_print(
            command=NAME,
            message=INFO_MESSAGE("The virtual environment already exists so a new one won't be created")
        )

    else:
        caos_command_print(command=NAME, message=INFO_MESSAGE("Creating a new virtual environment..."))
        create_env_process: subprocess.CompletedProcess = subprocess.run(
            [sys.executable, "-m", "venv", os.path.abspath(get_current_dir()+"/"+env_name)],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )

        if create_env_process.returncode != 0:
            raise CreateVirtualEnvironmentException(create_env_process.stderr)

        caos_command_print(command=NAME, message=SUCCESS_MESSAGE("A new virtual environment was created"))

    if is_win_os():
        if not os.path.isfile(PIP_PATH_VENV_WIN.replace("venv", env_name)):
            caos_command_print(
                command=NAME,
                message=WARNING_MESSAGE("The virtual environment does not have a 'pip' binary")
            )

        if not os.path.isfile(PYTHON_PATH_VENV_WIN.replace("venv", env_name)):
            raise MissingBinaryException("The virtual environment does not have a 'python' binary")

    if is_posix_os():
        if not os.path.isfile(PIP_PATH_VENV_POSIX.replace("venv", env_name)):
            caos_command_print(
                command=NAME,
                message=WARNING_MESSAGE("The virtual environment does not have a 'pip' binary")
            )

        if not os.path.isfile(PYTHON_PATH_VENV_POSIX.replace("venv", env_name)):
            raise MissingBinaryException("The virtual environment does not have a 'python' binary")


def main(args: List[str]) -> ExitCode:
    try:
        if not is_supported_os():
            raise UnsupportedOS("Only Windows and UNIX Like OSs are supported")

        virtual_env_name: str = args[0] if len(args) >= 1 else None
        current_dir: str = get_current_dir()
        create_caos_yaml(current_dir=current_dir, env_name=virtual_env_name)
        create_virtual_env(current_dir=current_dir)

    except Exception as e:
        caos_command_print(command=NAME, message=ERROR_MESSAGE("<<{}>> {}".format(type(e).__name__, str(e))))
        return ExitCode(1)
    return ExitCode(0)