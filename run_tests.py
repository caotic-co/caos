import os
from tests import run, exceptions

def is_win_os() -> bool:
    return os.name == "nt"


def is_posix_os() -> bool:
    return os.name == "posix"


def is_supported_os() -> bool:
    return is_win_os() or is_posix_os()


if __name__ == "__main__":
    if is_supported_os():
        run.main()
    else:
        raise exceptions.UnsupportedOS("Only Windows and UNIX Like OSs are supported")
