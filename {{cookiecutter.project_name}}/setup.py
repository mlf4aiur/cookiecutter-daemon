#!/usr/bin/env python

"""
Setup script for {{cookiecutter.project_name}}.
"""

import os
import setuptools

from {{cookiecutter.project_name}} import __project__, __version__

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

install_requires = [
    # List your project dependencies here.
    # For more details, see:
    # http://packages.python.org/distribute/setuptools.html#declaring-dependencies
    'Fabric',
    'nose'
]


setuptools.setup(
    name=__project__,
    version=__version__,

    description='{{cookiecutter.project_name}} is a daemon tool.',
    author='{{cookiecutter.full_name}}',
    author_email='{{cookiecutter.email}}',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},

    long_description=README,
    license="BSD License",

    install_requires=install_requires,
)
