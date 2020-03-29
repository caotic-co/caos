import os
import sys
import subprocess
from typing import List, NewType
from caos.utils.working_directory import get_current_dir
from caos.style.console import caos_command_print, red_text, yellow_text, green_text
from .exceptions import CreateVirtualEnvironmentException
from .constants import (
    NAME, _DEFAULT_VIRTUAL_ENVIRONMENT_NAME, _CAOS_YAML_FILE_NAME, _CAOS_YAML_TEMPLATE
)

ExitCode = NewType("ExitCode", int)


def create_virtual_env(current_dir:str, env_name: str) -> str:
    if os.path.isdir("{CURRENT_DIR}/{ENV_NAME}".format(CURRENT_DIR=current_dir, ENV_NAME=env_name)):
        caos_command_print(command=NAME, message=yellow_text("INFO: Virtual environment already exists"))
        return "venv_exists"

    caos_command_print(command=NAME, message="Creating virtual environment...")
    create_env_process: subprocess.CompletedProcess = subprocess.run(
        [sys.executable, "-m", "venv", os.path.abspath(get_current_dir()+"/"+env_name)],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    if create_env_process.returncode != 0:
        raise CreateVirtualEnvironmentException(create_env_process.stderr)

    caos_command_print(command=NAME, message=green_text("SUCCESS: Virtual environment created"))
    return "ok"


def create_caos_yaml(current_dir:str, env_name: str) -> str:
    caos_yml_path: str = "{CURRENT_DIR}/{CAOS_YAML}".format(CURRENT_DIR=current_dir, CAOS_YAML=_CAOS_YAML_FILE_NAME);
    if os.path.isfile(caos_yml_path):
        caos_command_print(
            command=NAME,
            message=yellow_text("INFO: '{CAOS_YAML}' already exists".format(CAOS_YAML=_CAOS_YAML_FILE_NAME))
        )
        return "yaml_exists"

    caos_command_print(command=NAME, message="Creating '{CAOS_YAML}'...".format(CAOS_YAML=_CAOS_YAML_FILE_NAME))

    with open(file=caos_yml_path, mode="w") as caos_yml_file:
        caos_yml_file.write(
            _CAOS_YAML_TEMPLATE.format(VENV_NAME=env_name)
        )

    caos_command_print(
        command=NAME,
        message=green_text("SUCCESS: '{CAOS_YAML}' created".format(CAOS_YAML=_CAOS_YAML_FILE_NAME))
    )

    return "ok"


def main(args: List[str]) -> ExitCode:
    try:
        virtual_env_name: str = args[0] if len(args) >= 1 else _DEFAULT_VIRTUAL_ENVIRONMENT_NAME
        current_dir:str  = get_current_dir()
        creation_code_venv: str = create_virtual_env(current_dir=current_dir, env_name=virtual_env_name)
        creation_code_yaml: str = create_caos_yaml(current_dir=current_dir, env_name=virtual_env_name)

        if creation_code_venv == "ok" and creation_code_yaml == "yaml_exists":
            caos_command_print(
                command=NAME,
                message=yellow_text(
                    "INFO: Don't forget to update the '{CAOS_YAML}' file to point to the right virtual environment"
                    .format(CAOS_YAML=_CAOS_YAML_FILE_NAME)
                )
            )


    except Exception as e:
        caos_command_print(command=NAME, message=red_text("ERROR <<{}>>:\n{}".format(type(e).__name__, str(e))))
        return ExitCode(1)
    return ExitCode(0)