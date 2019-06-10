
<p align="center">
    <a href="https://github.com/ospinakamilo/caos" target="_blank">
        <img src="https://github.com/ospinakamilo/caos/blob/master/src/docs/img/caos_logo.svg" height="100px">
    </a>
    <h1 align="center">CAOS</h1>
    <br>
    <p align="center">Simple Dependency Management for <b>Python 3</b> Projects using <b>pip</b> and <b>virtualenv</b>.</p>
</p>

Requirements
------------

For this project to work you need to have installed **Python >= 3.5**, **pip** and **virtualenv**.
 

Dependencies 
------------
If you are using Python 3 in **Windows** there are no dependencies for you to install.
If you are using **Linux** make sure to install **pip** and **virtualenv** first.
#### Fedora
~~~
sudo dnf install python3-pip python3-virtualenv
~~~

#### Ubuntu
~~~
sudo apt-get install python3-pip python3-venv
~~~

#### Open Suse
~~~
sudo zypper install python3-pip python3-virtualenv
~~~

Installation
------------
If you already installed **pip** and **virtualenv** use the next command to install **caos**.

### Windows
In a command prompt with administrative rights type:
~~~
pip3 install caos
~~~

### Linux
In a terminal window type:
~~~
sudo pip3 install caos
~~~

Usage
------------
Once installed you can use "caos" trough the command line

**Arguments**
 - **init** - Create the .json template file for the project
 - **prepare** - Create a new virtual environment
 - **update** - Download the project dependencies
 - **check** - Validate the downloaded dependencies
 - **test** - Run all the unit tests using th unittest framework
 - **run** - Execute the main entry point script for the project
 - **--help, -h** - Get documentation about the arguments and usage
 - **--version, -v** - Show the installed version

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
username@host:~$ caos check    #Validate the dependencies have been downloaded
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
username@host:~$ caos --help     #Get a similar set of instructions to the ones shown here
```
```console
username@host:~$ caos --version  #Display the current installed version
```

Youtube Tutorial
------------
<https://youtu.be/rn25t6uT150>
