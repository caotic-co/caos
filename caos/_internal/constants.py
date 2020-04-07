import os
from enum import Enum
from caos._internal.utils.working_directory import get_current_dir

_CURRENT_DIR = get_current_dir()

DEFAULT_VIRTUAL_ENVIRONMENT_NAME: str = "venv"
VIRTUAL_ENVIRONMENT_NAME_REGEX: str = r"^(\w)+$"
PYTHON_PATH_VENV_POSIX = os.path.abspath(_CURRENT_DIR+"/"+DEFAULT_VIRTUAL_ENVIRONMENT_NAME+"/bin/python")
PYTHON_PATH_VENV_WIN = os.path.abspath(_CURRENT_DIR+"/"+DEFAULT_VIRTUAL_ENVIRONMENT_NAME+"/Scripts/python.exe")
PIP_PATH_VENV_POSIX = os.path.abspath(_CURRENT_DIR+"/"+DEFAULT_VIRTUAL_ENVIRONMENT_NAME+"/bin/pip")
PIP_PATH_VENV_WIN = os.path.abspath(_CURRENT_DIR+"/"+DEFAULT_VIRTUAL_ENVIRONMENT_NAME+"/Scripts/pip.exe")

CAOS_YAML_FILE_NAME = "caos.yml"


class ValidDependencyVersionRegex(Enum):
    MAJOR_MINOR_PATCH = r"^(\^|\~)?(\d+\.)(\d+\.)(\d+)$"  # (^| ~) X.X.X
    MAJOR_MINOR = r"^(\^|\~)?(\d+\.)(\d+)$"  # (^| ~) X.X
    MAJOR = r"^(\^|\~)?(\d+)$"  # (^| ~) X
    LATEST = r"^(latest|LATEST)$"  # latest or LATEST
    WHL = r"^(.+)(\.whl|\.WHL)$"  # Anything.whl or Anything.WHL
