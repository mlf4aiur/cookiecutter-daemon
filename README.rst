cookiecutter-daemon
===================

Cookiecutter template for a Python daemon package. See https://github.com/audreyr/cookiecutter.

Quick start
-----------

Generate a Python package project::

    pip install cookiecutter
    cookiecutter https://github.com/mlf4aiur/cookiecutter-daemon.git


Follow following step to setup your development environment.

- Use virtualenv to create isolated Python environments::

    sudo pip install virtualenv
    virtualenv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    rm -rf .git

- Create your own requirements.txt::

    pip freeze | awk -F = '{print $1}' > requirements.txt

- Upgrade packages to latest version::

    pip install -U -r requirements.txt

- Testing code::

    # nose
    nosetests
    # Fabric
    fab test
    # setuptools
    python setup.py test

- create a new source distribution as tarball::

    python setup.py sdist --formats=gztar
    # Fabric
    fab pack

- Deploying your code::

    fab pack deploy

Contributing
------------

- Fork it
- Create your feature branch (git checkout -b my-new-feature)
- Commit your changes (git commit -am 'Add some feature')
- Push to the branch (git push origin my-new-feature)
- Create new Pull Request

Bugs
----
If you find a bug please report it. Verify that it hasn't `already been submitted <https://github.com/mlf4aiur/cookiecutter-daemon/issues>`_ and then `log a new bug <https://github.com/mlf4aiur/cookiecutter-daemon/issues/new>`_. Be sure to provide as much information as possible.

Credits
-------

This python daemon library is a fork of the `python-daemon <https://github.com/serverdensity/python-daemon>`_.
