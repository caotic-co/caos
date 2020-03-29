import os
import sys
import subprocess
from tests.exceptions import UnsupportedOS, CreateVirtualEnvironmentException

###### Constants ######
_VENV_NAME_WIN = "venv-win"
_VENV_NAME_POSIX = "venv-posix"


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
        if not is_win_venv_present():
            print("Creating virtual environment...")
            create_env_process: subprocess.CompletedProcess = subprocess.run(
                [sys.executable, "-m", "venv", _VENV_NAME_WIN],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True
            )

            if create_env_process.returncode != 0:
                raise CreateVirtualEnvironmentException(create_env_process.stderr)
        return

    elif is_posix_os():
        if not is_posix_venv_present():
            print("Creating virtual environment...")
            create_env_process: subprocess.CompletedProcess = subprocess.run(
                [sys.executable, "-m", "venv", _VENV_NAME_POSIX],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                universal_newlines=True
            )

            if create_env_process.returncode != 0:
                raise CreateVirtualEnvironmentException(create_env_process.stderr)
        return

    raise UnsupportedOS("Only Windows and UNIX Like OSs are supported")


def get_python_path() -> str:
    create_venv_if_missing()
    if is_win_os():
        return "{VIRTUAL_ENV}/Scripts/python.exe".format(VIRTUAL_ENV=_VENV_NAME_WIN)
    elif is_posix_os():
        return "{VIRTUAL_ENV}/bin/python".format(VIRTUAL_ENV=_VENV_NAME_POSIX)


if __name__ == "__main__":
    print(os.environ.get("PATH"))
    python: str = get_python_path()
    tests: str = "from tests.run import main; main()"
    execute_tests: subprocess.CompletedProcess = subprocess.run(
        [python, "-c", tests] + sys.argv
    )
    exit(execute_tests.returncode)
