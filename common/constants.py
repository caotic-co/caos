import os
import common.utils

_LINUX_UNIX = 'linux_unix'
_WINDOWS = 'windows'
_UNSUPPORTED = 'unsupported'

#PYTHON VENV
_CURRENT_OS = common.utils.get_os_type()
if _CURRENT_OS == _LINUX_UNIX:
    _PYTHON_PATH = '"{0}"'.format(os.path.abspath(path="../caos/venv/bin/python"))
elif _CURRENT_OS == _WINDOWS:
    _PYTHON_PATH = '"{0}"'.format(os.path.abspath(path="../caos/venv/Scripts/python.exe"))


#PROJECT PATHS
_PROJECT_PATH = os.path.abspath(path="../caos")
_SRC_PATH = os.path.abspath(path="../caos/src")
_ENTRY_POINT = os.path.abspath(path="../caos/src/__main__.py")
_OUT_TEST = os.path.abspath(path="../caos/tests/out_test")