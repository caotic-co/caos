"""update - Update and download the virtual environment dependencies according to the json file"""

import os
import re
import json
import subprocess
import common
from caos._internal.exceptions import (
    VenvNotFound, VenvBinariesMissing, InvalidJSON, MissingJSONKeys,
    InvalidVersionFormat, InvalidMainScriptPath, InvalidTestsPath, DownloadDependenciesError
)

_console_messages={
    "success":"Success: Virtual environment updated",
    "fail": "Fail: Virtual environment could not be updated",
    "no_json_found": "Fail: caos.json does not exist. To create it run 'caos init'",
    "no_venv_found": "Fail: Virtual environment does not exist. To create it run 'caos prepare'",
    "missing_venv_binaries": "Fail: The virtual environment is missing some binaries. Try creating it again",
    "invalid_json": "Fail: caos.json is invalid or has syntax errors",
    "json_mising_keys": "Fail: caos.json is missing the required keys for it to be valid",
    "version_format_error": "Fail: At least one package inside caos.json has a wrong version format, the valid format is n.n.n",
    "missing_main": "Fail: The path inside caos.json for the main script does not exist",
    "missing_tests": "Fail: The path inside caos.json for running tests does not exist",
    "downloading": "In Progress: Downloading dependencies...",
    "download_error": "Fail: There was an error and the dependencies could not be downloaded",
    "permission_error": "Fail: Virtual environment could not be updated due to permission errors",
}

def _json_exists() -> bool:
    exists = os.path.isfile(path=common.constants._CAOS_JSON_FILE)
    return True if exists else False

def _venv_exists() -> bool:
    exists = os.path.isdir(common.constants._CAOS_VENV_DIR)
    return True if exists else False

def _are_venv_binaries_available() -> bool:
    exists_python = os.path.isfile(path=common.constants._PYTHON_PATH)
    exists_pip = os.path.isfile(path=common.constants._PIP_PATH)
    exists_activate = os.path.isfile(path=common.constants._ACTIVATE_PATH)
    return exists_python and exists_pip and exists_activate

def _read_json_file() -> dict:
    try:
        with open(file=common.constants._CAOS_JSON_FILE, mode="r") as json_file:  
            return json.load(json_file)
    except Exception:
        raise InvalidJSON()

def _is_json_syntax_correct(json_data:dict) -> bool:
    all_keys_exist = set(common.constants._CAOS_JSON_KEYS).issubset(json_data)
    if all_keys_exist:
        return True
    return False

def _are_packages_versions_format_valid(json_data:dict) -> bool:
    for version in json_data[common.constants._CAOS_JSON_REQUIRE_KEY].values():        
        match_pattern= False
        for pattern in common.constants._CAOS_JSON_PACKAGE_VERSION_PATTERNS:
            if re.match(pattern, version):
                match_pattern = True
                break 
        if match_pattern or version in common.constants._CAOS_JSON_PACKAGE_VALID_VERSIONS:
            return True
    return False

def _main_file_exists(json_data:dict) -> bool:
    exists = os.path.isfile(path=json_data[common.constants._CAOS_JSON_MAIN_KEY])
    if exists:
        return True
    else:
        return False

def _tests_folder_exists(json_data:dict) -> bool:
    exists = os.path.isdir(json_data[common.constants._CAOS_JSON_TESTS_KEY])
    if exists:
        return True
    else:
        return False

def _download_and_updated_packages(json_data:dict) -> None:
    packages = []
    for p, v in json_data[common.constants._CAOS_JSON_REQUIRE_KEY].items():
        if v == common.constants._CAOS_LATEST_VERSION:
            package = p          
        else:
            package = "{0}=={1}".format(p,v)

        packages.append(package)

    
    a=subprocess.run(
        [common.constants._PYTHON_PATH, "-m", "pip", "install", "--force-reinstall", "pip"],
        capture_output=True,
        universal_newlines=True,
        shell=True
    )
    
    download_dependencies_process = subprocess.run(
        [common.constants._PYTHON_PATH, "-m", "pip", "install", "--force-reinstall"] + packages,
        capture_output=True,
        universal_newlines=True,
        shell=True
    )

    if download_dependencies_process.stderr:      
        raise DownloadDependenciesError()
    






def update_dependencies() -> None:
    try:
        if not _json_exists():            
            raise FileNotFoundError()
        
        if not _venv_exists():            
            raise VenvNotFound()        

        if not _are_venv_binaries_available():
            raise VenvBinariesMissing()
        
        json_data = _read_json_file() # Raise InvalidJSON

        if not _is_json_syntax_correct(json_data=json_data):
            raise MissingJSONKeys()
        
        if not _are_packages_versions_format_valid(json_data=json_data):
            raise InvalidVersionFormat()
        
        if not _main_file_exists(json_data=json_data):
            raise InvalidMainScriptPath()
        
        if not _tests_folder_exists(json_data=json_data):
            raise InvalidTestsPath()

        print(_console_messages["downloading"])
        _download_and_updated_packages(json_data=json_data) # Raise DownloadDependenciesError
        print(_console_messages["success"])
        
    except FileNotFoundError:
        print(_console_messages["no_json_found"])
    except VenvNotFound:
        print(_console_messages["no_venv_found"])
    except VenvBinariesMissing:
        print(_console_messages["missing_venv_binaries"])
    except InvalidJSON:
        print(_console_messages["invalid_json"])
    except MissingJSONKeys:
        print(_console_messages["json_mising_keysprint"])
    except InvalidVersionFormat:
        print(_console_messages["version_format_error"])
    except InvalidMainScriptPath:
        print(_console_messages["missing_main"])
    except InvalidTestsPath:
        print(_console_messages["missing_tests"])
    except DownloadDependenciesError:
        print(_console_messages["download_error"])
    except PermissionError:
        print(_console_messages["permission_error"])
    except Exception:
        print(_console_messages["fail"])