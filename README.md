<p align="center">
    <a href="https://github.com/ospinakamilo/caos" target="_blank">
        <img src="https://github.com/ospinakamilo/caos/blob/master/docs/img/caos_logo.svg" height="100px">
    </a>
    <h1 align="center">CAOS</h1>
    <br>
</p>
Simple Dependencies Manager for Python3 Projects

REQUIREMENTS
------------

The minimum requirements for this project is to have installed Python >= 3.5
with the following dependencies updated:
    -pip
    -virtualenv


Installation using PIP
------------
Run the following command if you have access to pip
~~~
pip install caos
~~~
or run this command to use pip as a python module

~~~
python -m pip install caos
~~~


Manual Installation
------------
Clone the repository using the following command:
~~~
git clone https://github.com/ospinakamilo/caos
~~~

In the location where you cloned the repository run the next command:
~~~
python setup.py bdist_wheel
~~~
This will create a folder called 'dist' which contatins the module to install.
To install the module in your local system use the following commmand (be sure to validate the version number in the file):
~~~
python -m pip install dist/caos-x.x-py3-none-any.whl
~~~

Unit Testing
------------
To run the unit tests for the source code go the root of the cloned project "caos/" and run
~~~
python -m unittest discover .\tests
~~~

Usage
------------
Once installed you can use "caos" trough the command line

Arguments
    init
        Create the .json template file for the project
    prepare
        Create a virtual environment and download the project dependencies
    test
        Run all the unit tests
    run
        Execute the main entry point script for the project

Examples
    Create the caos.json file in the current directory
    ~~~
    caos init
    ~~~
        
    Set up a virtual environment with the project dependencies
    ~~~
    caos prepare
    ~~~
        
    Execute all the unit tests available
    ~~~
    caos test
    ~~~
        
    Run the main script of the project
    ~~~
    caos run
    ~~~
        
    Run the main script of the project sending some arguments 
    ~~~
    caos run arg1 arg2
    ~~~
        
