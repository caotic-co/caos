import os


###### Constants ######
_VENV_NAME_WIN = "venv-win"
_VENV_NAME_POSIX = "venv-posix"


###### Classes ######
class UnsupportedOS(Exception):
    pass


###### Functions ######
def is_win_os() -> bool:
    return os.name == "nt"


def is_posix_os() -> bool:
    return os.name == "posix"


def is_supported_os() -> bool:
    return is_win_os() or is_posix_os()


def is_win_venv_present() -> bool:
    return os.path.isdir(_VENV_NAME_WIN)


def is_posix_venv_present() -> bool:
    return os.path.isdir(_VENV_NAME_POSIX)


def create_venv_if_missing() -> None:
    if is_win_os():
        if is_win_venv_present():
            return

    elif is_posix_os():
        if is_win_venv_present():
            return

    raise UnsupportedOS("Only Windows and UNIX Like OSs are supported")


def main() -> None:
    _ERROR_FORMAT = "[Exception Type: '{ex_type}'] -> {ex_message}"
    _SUCCESS_FORMAT = "[No errors found] -> {message}"

    try:
        create_venv_if_missing()
        print(_SUCCESS_FORMAT.format(message="Tests execution completed successfully"))

    except Exception as e:
        print(_ERROR_FORMAT.format(
            ex_type=type(e).__name__,
            ex_message=str(e)
        ))
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
