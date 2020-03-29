import pprint
from caos.style.console import *
from caos._third_party.pyyaml_5_3_1 import yaml

print(CAOS_CONSOLE_LOGO)
caos_command_print(command="prepare", message="Updating..")
caos_command_print(command="ERROR", message="Something went wrong...")
caos_command_print(command="ERROR", message="Warning message..")
caos_command_print(command="unittest", message="Testing.. everything")


caos_yaml = {
    "caos":{
        "dependencies":{
            "numpy": "latest",
            "flask": "1.1.1"
        },
        "tasks": {
            "run": {
                "command": "caos python ./main.py"
            },
            "unittest": {
                "command": "caos unittest ./",
            },

            "build": {
                "commands": [
                    "exec command1",
                    "exec command2",
                    "exec command3"
                ]
            }
        }
    }
}

with open("tests/tmp/caos_template.yml", "r") as file:
    pprint.pprint(yaml.load(stream=file.read(), Loader=yaml.FullLoader))
