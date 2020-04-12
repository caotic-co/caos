## Table of Contents
1. [Usage](#usage)
    1. [Init](#init)   
    2. [Update](#update)
    3. [Check](#check)
    3. [Run](#run)
    4. [Python](#python)
    5. [Pip](#pip)
    6. [Version](#version)
    7. [Help](#help)
2. [Contribute](#contribute)     
    1. [Setup a Local Environment](#setup-a-local-environment)   
    2. [Unit Testing](#unit-testing)
    3. [Upload to PyPi](#upload-to-pypi)

## Usage
### Init
Creates a Python virtual environment based on the configuration
of an existing 'caos.yml' file in the current directory.

If the 'caos.yml' file is not present in the current directory a
new virtual environment and configuration file are created.
~~~~
$ caos init
$ caos init [VIRTUAL_ENV_NAME]
~~~~

### Update
Downloads the missing dependencies of the project
and upgrades the ones with newer minor or patch versions,
according to the defined configuration.

It requires an existing 'caos.yml' file and a virtual
environment in the current directory.
~~~~
$ caos update
~~~~

### Check
Validates if the dependencies for the project are installed
in the virtual environment.

It requires an existing 'caos.yml' file and a virtual
environment in the current directory.
~~~~
$ caos check
~~~~

### Run
Execute a task defined within the 'caos.yml' file.
~~~~
$ caos run [TASK_NAME]
~~~~

### Python
A shortcut for calling the Python binary of the project.

It requires an existing 'caos.yml' file and a virtual
environment in the current directory.
~~~~
$ caos python
$ caos python [SCRIPT_FILE]
$ caos python [SCRIPT_FILE] [ARG]
~~~~

### Pip
A shortcut for calling the PIP binary of the project.

It requires an existing 'caos.yml' file and a virtual
environment in the current directory.
~~~~
$ caos python
$ caos python [SCRIPT_FILE]
$ caos python [SCRIPT_FILE] [ARG]
~~~~

### Version
Shows the currently installed version
~~~~
$ caos --version
$ caos -v
$ caos -V
~~~~

### Help
Shows documentation about the available arguments and their usage
~~~~
$ caos --help
$ caos -h
~~~~

## Contribute   
### Setup a Local Environment 
Make sure to have Python>=3.6 and virtualenv installed and then clone the repository using the following command:
~~~
$ git clone https://github.com/caotic-co/caos
~~~

### Unit Testing
To execute the tests of the project use the following command:
~~~
$ python run_tests.py
~~~
    
    
### Upload to PyPi
Install the required dependencies:
~~~
$ pip install --upgrade pip setuptools wheel
$ pip install tqdm
$ pip install --upgrade twine
~~~


In the location where you cloned the repository run the next command:
~~~
$ python setup.py sdist bdist_wheel
~~~
This will create a folder called 'dist' which contains the module to install.
To install the module in your local system use the following commmand (be sure to validate the version number in the file):
~~~
$ pip install dist/caos-x.x.x.tar.gz # Optional
~~~

Use the following command to upload to the PyPi repository:
~~~
$ python -m twine upload dist/*
~~~






    