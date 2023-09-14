import os
import sys
import json
import subprocess
from io import StringIO
from typing import List
from caos._internal.types import ExitCode
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.yaml import get_tasks_from_yaml, Tasks
from caos._internal.constants import CAOS_YAML_FILE_NAME
from caos._internal.exceptions import MissingYamlException
from caos._internal.console import caos_command_print, WARNING_MESSAGE
from .exceptions import MissingTaskArgument, TaskNotFound, StepExecutionError
from .constants import NAME


def main(args: List[str], cwd_step: str = None, env_step: dict = None) -> ExitCode:
    current_dir: str = get_current_dir()
    if not os.path.isfile(os.path.abspath(current_dir + "/" + CAOS_YAML_FILE_NAME)):
        raise MissingYamlException("No '{}' file found. Try running first 'caos init'".format(CAOS_YAML_FILE_NAME))

    if len(args) < 1:
        raise MissingTaskArgument("No task name to execute was given")

    task_name: str = args[0]

    available_tasks: Tasks = get_tasks_from_yaml()

    if not task_name in available_tasks:
        raise TaskNotFound("No task named '{}' was found".format(task_name))

    if len(args) > 1:
        caos_command_print(
            command=NAME,
            message=WARNING_MESSAGE("The tasks can't receive arguments")
        )

    steps: List[str] = available_tasks[task_name]

    caos_context_env_var = "_CAOS_CONTEXT="

    added_caos_commands = f"{sys.executable} -c \"import os; os.environ['_CAOS_PWD']=os.getcwd();print('{caos_context_env_var}'+str(dict(os.environ)))\""

    is_unittest: bool = True if isinstance(sys.stdout, StringIO) else False
    for step in steps:
        if step in available_tasks:
            main(args=[step], cwd_step=cwd_step, env_step=env_step)
            continue

        step_process: subprocess.CompletedProcess = subprocess.run(
            f"{step} && {added_caos_commands}",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=sys.stdin,
            cwd=cwd_step,
            env=env_step,
            universal_newlines=True,
            shell=True
        )

        if step_process.returncode != 0:
            raise StepExecutionError("Within the task '{}' the step '{}' returned a non zero exit code"
                                     .format(task_name, step))

        if step_process.stdout.startswith(caos_context_env_var):
            caos_preserved_context_str = step_process.stdout.replace(caos_context_env_var, "")
        else:
            command_output, caos_preserved_context_str = step_process.stdout.split(caos_context_env_var)
            print(command_output)

        caos_preserved_context_str.replace("\n", "")

        if not caos_preserved_context_str:
            caos_preserved_context_str = "{}"

        env_step = json.loads(caos_preserved_context_str.replace("'", '"'))
        cwd_step = env_step["_CAOS_PWD"]

    return ExitCode(0)
