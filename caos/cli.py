import sys
from importlib import import_module
from textwrap import dedent
from types import ModuleType
from typing import List, NewType
from caos.cli_commands import available_commands
from caos.style.console import CAOS_CONSOLE_LOGO

__VERSION__ = "2.0.0"

ExitCode = NewType("ExitCode", int)


def show_version() -> None:
    print("You are using caos version {}".format(__VERSION__))


def get_commands() -> List[ModuleType]:
    """Get a list of all commands available for caos to use"""
    modules:  List[ModuleType] = []
    command_name: str
    for command_name in available_commands:
        modules.append(import_module("caos.cli_commands.{}".format(command_name)))
    return modules


def show_help() -> None:
    """"Print the available documentation for the existing commands"""
    _HEADER: str = dedent('''    
        DESCRIPTION
            A simple dependency management tool and tasks executor for python
            
        PROGRAM INFORMATION
            --help or -h
                Shows documentation about the available arguments and its usage
            --version, -v or -V
                Shows the currently installed version
    ''')

    print(dedent(CAOS_CONSOLE_LOGO)[1:]+(" "*28)+"v{}".format(__VERSION__))
    print(_HEADER)

    _COMMAMD_HELP_FORMAT: str = dedent('''\
        ARGUMENTS
            {COMMAND_NAME}
                Description:
                    {COMMAND_DESCRIPTION}                
                Usage Example:''')

    command_module: ModuleType
    for command_module in get_commands():
        print(_COMMAMD_HELP_FORMAT.format(
            COMMAND_NAME=command_module.NAME.strip(),
            COMMAND_DESCRIPTION=command_module.DESCRIPTION.strip()
        ))

        print(command_module.CLI_USAGE_EXAMPLE)


def get_command(command: str) -> ModuleType:
    command_module: ModuleType
    for command_module in get_commands():
        if command == command_module.NAME:
            return command_module
    return None


def cli_entry_point() -> ExitCode:
    """CLI entry point that calls the required commands specified by the user """
    if not sys.argv[1:]:
        print("No argument given, if you need help try typing 'caos --help'")
        return ExitCode(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command in ("--help", "-h"):
        show_help()

    elif command in ("--version", "-v", "-V"):
        show_version()

    else:
        requested_command: ModuleType = get_command(command=command)
        if not requested_command:
            print("Unknown argument, if you need help try typing 'caos --help'")
            return ExitCode(1)

        return ExitCode(requested_command.entry_point(args=args))

    return ExitCode(0)
