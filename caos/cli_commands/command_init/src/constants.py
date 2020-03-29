NAME: str = "init"
DESCRIPTION: str = "Creates the Python virtual environment and 'caos.yml' file if not present in the current folder"
CLI_USAGE_EXAMPLE: str = """\
            caos init
                Creates a python virtual environment under the name 'venv'        
            caos init [ENV_NAME]
                Creates a python virtual environment under a given name
"""

_DEFAULT_VIRTUAL_ENVIRONMENT_NAME: str = "venv"

_CAOS_YAML_FILE_NAME = "caos.yml"

_CAOS_YAML_TEMPLATE="""\
virtual_environment: "{VENV_NAME}"

dependencies:
  pip: "latest"
#  requests: "~2.0" # Allow only Minor version changes
#  flask: "~1.1.0"  # Allow only Patch version changes
#  numpy: "1.18.2"  # Allow only Exact version
#  tensorflow_1_13_1: "./local_libs/tensorflow-1.14.0-py3-none-any.whl" # Local WHl
#  tensorflow_1_14_0: "https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.14.0-py3-none-any.whl" # Remote WHl

tasks:
#  test:
#    - "caos unittest ./"
#
#  run:
#    - "caos python ./main.py"
#
#  test_and_run:
#    - test
#    - run
#    - "echo 'Done'"
"""
