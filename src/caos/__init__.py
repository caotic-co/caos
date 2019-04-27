import sys

_valid_commands=["--help"]

def console() -> None:
    '''
    caos command line arguments
    '''
    if len(sys.argv) <= 1:
        print("Need help? try using --help")
        return

    args = sys.argv[1:]
    
    if args[0] not in _valid_commands:
        print("Unknown Argument {0}".format(args[0]))
        print("Need help? try using --help")
        return
    
    
        