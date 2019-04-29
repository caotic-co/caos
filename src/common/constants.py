import os
import common.utils

_LINUX_UNIX = 'linux_unix'
_WINDOWS = 'windows'
_UNSUPPORTED = 'unsupported'

#CAOS files and folders
_CAOS_JSON_FILE = "./caos.json"
_CAOS_VENV_DIR = "./venv"

#CAOS PYTHON VENV
_CURRENT_OS = common.utils.get_os_type()
if _CURRENT_OS == _LINUX_UNIX:
    _VENV_BINARIES_PATH = os.path.abspath(path=_CAOS_VENV_DIR+ "/bin")
    _PYTHON_PATH = os.path.abspath(path=_CAOS_VENV_DIR+ "/bin/python")
    _PIP_PATH = os.path.abspath(path=_CAOS_VENV_DIR+ "/bin/pip")
    _ACTIVATE_PATH = os.path.abspath(path=_CAOS_VENV_DIR+ "/bin/activate")
elif _CURRENT_OS == _WINDOWS:
    _VENV_BINARIES_PATH = os.path.abspath(path=_CAOS_VENV_DIR+"/Scripts")
    _PYTHON_PATH = os.path.abspath(path=_CAOS_VENV_DIR+"/Scripts/python.exe")
    _PIP_PATH = os.path.abspath(path=_CAOS_VENV_DIR+"/Scripts/pip.exe")
    _ACTIVATE_PATH = os.path.abspath(path=_CAOS_VENV_DIR+"/Scripts/activate.bat")

#caos.json
_CAOS_JSON_REQUIRE_KEY = "require"
_CAOS_JSON_TESTS_KEY = "tests"
_CAOS_JSON_MAIN_KEY = "main"
_CAOS_JSON_KEYS = [_CAOS_JSON_REQUIRE_KEY, _CAOS_JSON_TESTS_KEY, _CAOS_JSON_MAIN_KEY]
_CAOS_JSON_PACKAGE_VERSION_PATTERNS = [
    "^(\d+\.)?(\d+\.)?(\d+)$", # x.x.x
    "^(\d+\.)?(\d+)$"          # x.x
]
_CAOS_LATEST_VERSION = "latest"
_CAOS_JSON_PACKAGE_VALID_VERSIONS = [_CAOS_LATEST_VERSION]     