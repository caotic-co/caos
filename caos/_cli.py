import sys
from types import ModuleType
from typing import NewType
from caos._cli_commands import help_command, version_command
from caos._internal.utils.commands import get_command


ExitCode = NewType("ExitCode", int)

def cli_entry_point() -> ExitCode:
    """CLI entry point that calls the required commands specified by the user """
    if not sys.argv[1:]:
        print("No argument given, if you need help try typing 'caos --help'")
        return ExitCode(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command in ("--help", "-h"):
        help_command.show_help()

    elif command in ("--version", "-v", "-V"):
        version_command.show_version()

    else:
        requested_command: ModuleType = get_command(command=command)
        if not requested_command:
            print("Unknown argument, if you need help try typing 'caos --help'")
            return ExitCode(1)

        return ExitCode(requested_command.entry_point(args=args))

    return ExitCode(0)
