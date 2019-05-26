Manual Install
------------
Install the Dependencies
~~~
sudo python3 -m pip install --upgrade pip setuptools wheel
sudo python3 -m pip install tqdm
sudo python3 -m pip install --user --upgrade twine
~~~

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