from caos.utils.os import is_supported_os
from tests import run, exceptions


if __name__ == "__main__":
    if is_supported_os():
        print("Running tests...")
        run.main()
    else:
        raise exceptions.UnsupportedOS("Only Windows and UNIX Like OSs are supported")
