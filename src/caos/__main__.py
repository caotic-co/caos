"""Simple Dependencies Manager for Python3 Projects"""

import sys
from caos._internal import init, prepare, update

__all__=["console"]

_HELP = '''
    DESCRIPTION
        Simple Dependencies Manager for Python3 Projects

    ARGUMENTS
        init
            Create the .json template file for the project
        prepare
            Create a virtual environment and download the project dependencies
        test
            Run all the unit tests
        run
            Execute the main entry point script for the project

    EXAMPLES
        caos init
            Creates the caos.json file in the current directory

        caos prepare
            Set up a virtual environment with the project dependencies
        
        caos test
            Execute all the unit tests available
        
        caos run
            Run the main script of the project
        
        caos run arg1 arg2
            Run the main script of the project sending some arguments         
'''
_HELP_COMMAND = "help"
_INIT_COMMAND = "init"
_PREPARE_COMMAND = "prepare"
_UPDATE_COMMAND = "update"
_TEST_COMMAND = "test"
_RUN_COMMAND = "run"

_valid_commands=[_HELP_COMMAND, _INIT_COMMAND, _PREPARE_COMMAND, _UPDATE_COMMAND,_TEST_COMMAND, _RUN_COMMAND]

_console_messages={
    "need_help":"Unknown Argument, if you need help try typing 'caos help'",
    "help": _HELP,
}

def console() -> None:
    '''
    caos command line arguments
    '''
    if len(sys.argv) <= 1:
        print(_console_messages["need_help"])
        return

    args = [arg.lower() for arg in sys.argv[1:]]    
    command = args[0]

    if command not in _valid_commands:
        print(_console_messages["need_help"])
    elif command == _HELP_COMMAND:
        print(_console_messages["help"])
    elif command == _INIT_COMMAND:
        init.create_json()
    elif command == _PREPARE_COMMAND:
        prepare.create_venv()
    elif command == _UPDATE_COMMAND:
        update.update_dependencies()
    elif command == _TEST_COMMAND:
        pass
    elif command == _RUN_COMMAND:
        pass

if __name__ == "__main__":
    console()