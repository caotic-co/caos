
<p align="center">
    <a href="https://github.com/ospinakamilo/caos" target="_blank">
        <img src="https://github.com/ospinakamilo/caos/blob/master/src/docs/img/caos_logo.svg" height="100px">
    </a>
    <h1 align="center">CAOS</h1>
    <br>
    <p align="center">Simple Dependency Management for Python3 Projects</p>
</p>

Requirements
------------

The minimum requirements for this project is to have installed Python >= 3.5 with the following dependencies updated:

 - pip
 - virtualenv
 

Installation of Dependencies 
------------
If you are using Python 3 in **Windows** there are no dependencies for you to install.
If you are using **Linux** make sure to install Pip and Venv first.
#### Fedora
~~~
sudo dnf install python3-pip
~~~
~~~
sudo dnf install python3-virtualenv
~~~
#### Ubuntu
~~~
sudo apt-get install python3-pip
~~~
~~~
sudo apt-get install python3-venv
~~~
### Open Suse
~~~
zypper install python3-pip
~~~
~~~
zypper install python3-virtualenv
~~~


Installation of the library
------------
If you already installed the previous dependencies use the next command to install **caos** using pip.

### Windows
~~~
pip3 install caos
~~~

### Linux
~~~
sudo pip3 install caos
~~~


Manual Installation
------------
Clone the repository using the following command:
~~~
git clone https://github.com/ospinakamilo/caos
~~~

In the location where you cloned the repository run the next command:
~~~
python3 setup.py sdist bdist_wheel
~~~
This will create a folder called 'dist' which contains the module to install.
To install the module in your local system use the following commmand (be sure to validate the version number in the file):
~~~
python3 -m pip install dist/caos-x.x-py3-none-any.whl
~~~

Unit Testing
------------
To run the unit tests for the source code go the 'src' folder of the cloned project "caos/src/" and run
~~~
python3 -m unittest discover ./tests
~~~

Usage
------------
Once installed you can use "caos" trough the command line

**Arguments**
 - **init** - Create the .json template file for the project
 - **prepare** - Create a new virtual environment
 - **update** - Download the project dependencies
 - **test** - Run all the unit tests using th unittest framework
 - **run** - Execute the main entry point script for the project
 - **help** - Get documentation about the arguments and usage
 - **version** - Show the installed version

**Examples**
```console
username@host:~$ caos init     #Create the caos.json file in the current directory
```  
```console
username@host:~$ caos prepare  #Set up a new virtual environment
```
```console
username@host:~$ caos update   #Download the project dependencies into the virtual environment
``` 
```console
username@host:~$ caos test     #Execute all the unit tests available using the unnittest framework
```
 ```console
username@host:~$ caos run      #Run the main script of the project
```
```console
username@host:~$ caos run arg1 #Run the main script of the project sending some argument 
```
```console
username@host:~$ caos help     #Get a similar set of instructions to the ones shown here
```
```console
username@host:~$ caos version  #Display the current installed version
```

Youtube Tutorial
------------
<https://youtu.be/rn25t6uT150>
