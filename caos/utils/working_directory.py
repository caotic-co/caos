import os


def is_dev_environment() -> bool:
    """Returns True if the project source code structure is found in the working directory"""
    return os.path.isdir("caos") and \
                os.path.isdir("caos/cli_commands") and \
                os.path.isfile("caos/cli.py") and \
           os.path.isdir("docs") and\
           os.path.isdir("tests") and\
           os.path.isfile("LICENSE") and\
           os.path.isfile("caos.py")


def get_current_dir() -> str:
    if is_dev_environment():
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        os.chdir("tmp")
    return os.getcwd()