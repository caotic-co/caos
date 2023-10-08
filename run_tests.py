from caos._internal.utils.os import is_supported_os
from caos._internal.exceptions import UnsupportedOS
from tests import run


if __name__ == "__main__":
    if is_supported_os():
        print("[INFO] Running tests...")
        run.main()
    else:
        raise UnsupportedOS("[ERROR] Only Windows and UNIX Like OSs are supported")
