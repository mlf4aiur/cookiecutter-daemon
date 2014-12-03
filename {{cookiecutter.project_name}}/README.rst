{{cookiecutter.project_name}}
=============================

{{cookiecutter.project_short_description}}

Usage
-----

    ./skeleton.py -h
    usage: [-h] {start,stop,restart,status,foreground}

    Daemon tool

    positional arguments:
      {start,stop,restart,status,foreground}

    optional arguments:
      -h, --help            show this help message and exit

Build
-----

    python setup.py sdist --formats=gztar
