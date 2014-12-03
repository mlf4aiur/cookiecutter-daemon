#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import *


def test():
    local('python setup.py test')


def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar 2>/dev/null', capture=False)


def deploy():
    pass
