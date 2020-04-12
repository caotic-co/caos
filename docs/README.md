## Table of Contents
1. [Usage](#usage)
    1. [init](#init)   
    2. [update](#update)
    3. [check](#check)
    3. [run](#run)
    4. [python](#python)
    5. [pip](#pip)
2. [Contribute](#contribute)     
    1. [Setup a Local Environment](#setup-a-local-environment)   
    2. [Unit Testing](#unit-testing)
    3. [Upload to PyPi](#upload-to-pypi)

## Usage
### Init
~~~~
$ caos init
~~~~

### Update
~~~~
$ caos update
~~~~

### Check
~~~~
$ caos check
~~~~

### Run
~~~~
$ caos run
~~~~

### Python
~~~~
$ caos python
~~~~

### Pip
~~~~
$ caos pip
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






    