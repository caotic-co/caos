"""Init - Create the .json template file for the project"""

import os
from src.caos._internal.templates.caos_json import example_template

_console_messages={
    "success":"Success: caos.json created",
    "fail": "Fail: caos.json could not be created",
    "file_exists": "Fail: caos.json already exists"
}

def create_json():
    try:
        exists = os.path.isfile(path='./caos.json')
        if exists:
            raise FileExistsError()

        with open(file="./caos.json", mode="w") as caos_json_file:
            caos_json_file.write(example_template)
        print(_console_messages["success"])
    except FileExistsError:
         print (_console_messages["file_exists"])
    except Exception:
        print(_console_messages["fail"])
    