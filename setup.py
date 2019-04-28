import sys
from setuptools import find_packages, setup

full_description = '''
    Please take a look at our documentation for how to install and use caos:
        
        * `GitHub page`_
        .. _GitHub page: https://github.com/ospinakamilo/caos/
'''


setup(
    name="caos",  
    version="1.0",
    author="Team Camilo",
    author_email="camilo.ospinaa@gmail.com",
    description="caos - Simple Dependencies Manager for Python3 Projects",
    long_description=full_description,
    url="https://github.com/ospinakamilo/caos/",
    keywords='distutils easy_install egg setuptools wheel virtualenv dependencies manager ppm',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],

    package_dir={"": "src"},

    packages=find_packages(
        where="src",
        exclude=["docs", "tests"],
    ),    

    entry_points={
        "console_scripts": ["caos=caos:console"],
    },

    python_requires=">3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*,  <4",
    
 )