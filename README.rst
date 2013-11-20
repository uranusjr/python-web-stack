.. image:: https://travis-ci.org/uranusjr/python-web-stack.png?branch=master   :target: https://travis-ci.org/uranusjr/python-web-stack

=================
Python Web Stack
=================

A complete web stack for Python WSGI applications.

------
Scope
------

Only the default configuration of nginx from APT is supported now, although most POSIX-based use cases may be taken into consideration in the future. Windows support is possible (through Cygwin), but not planned yet.

-----------
Requisites
-----------

* nginx
* A capable C compiler, and Python's development files (``python-dev`` in APT). These are required because we need to roll our own uWSGI from PIP.
* virtualenv

++++++++++++++++++++++
No virtualenvwrapper?
++++++++++++++++++++++

Well you can always install it if you want to, don't you! This makes the setup minimal, and let us be able to configure things more freely. virtualenvwrapper requires some system integration (such as the ``WORKON_HOME`` environment variable) and is too fragile to user tweaks IMO.

------
Usage
------

All commands use an executable ``pywebstack`` as the interface. Possible subcommands include:

* ``mksite``
* ``rmsite``
* ``config``

Their respective behaviors are described below.

+++++++++++
``config``
+++++++++++

Configures various behaviours of the ``pywebstack`` command. The config values are saved to ``config.cfg`` inside the ``pywebstack`` module.

Name of each config should be a two-part string joined by a period. Examples include:

* ``virtualenv.root``
* ``nginx.available``
* ``nginx.enabled``

The ``config`` command can be used to read or write configs. To read a config value, use the following syntax::

    pywebstack config <config_name>

To write to a config, use this::

    pywebstack config <config_name> <value_to_write>

To remove a config, just assign it an empty string.

+++++++++++
``mksite``
+++++++++++

Creates a new WSGI site entry. The simplest command is::

    pywebstack mksite <project_type> <project_name>

This creates a project, a virtualenv (for the project), and appropriate uWSGI and nginx configuration files.

+++++++++++
``rmsite``
+++++++++++

Removes a site. Command syntax::

    pywebstack rmsite <project_name>

Note that ``pywebstack`` does **not** really track the projects you create, but rather just attempts to delete things when you run ``rmsite``. If you plan to mix custom projects and those managed by ``pywebstack`` in the same directory, you will be responsible to use correct names yourself so that custom things are not removed.

-----------------
Developing Notes
-----------------

To develop for Python Web Stack, you'll need some additonal packages aside from the dependencies. Run ``pip -r requirements/dev.txt`` to get it arranged.

++++++++++++++++++++++++
Submitting new formulae
++++++++++++++++++++++++

You are welcome to add new WSGI types to Python Web Stack. Just fork this project, add a new formula in ``pywebstack/formulae``, and send me a pull request. A valid formula should inherit from class ``formulae.Formula``, and override the following methods:

* ``get_wsgi_env``
* ``install``
* ``create_project``

You may also override additional methods to achieve additional customization. See the docstrings and comments inside ``formulae.Formula`` for details.

++++++++++++++++++++++
The ``manage`` script
++++++++++++++++++++++

A ``manage`` script is attached for some common tasks:

1. Run tests. ``manage test`` takes care of the ``nosetests`` arguments.
2. To run a ``pywebstack`` subcommand, instead of invoking ``bin/pywebstack mksite`` (or other subcommands) and setting up the correct ``PYTHONPATH`` manually, you can instead use ``manage mksite``.

-----
Todo
-----

Build a APT package. Dependencies:

* ``nginx``
* ``python-dev``
* ``python-virtualenv``
