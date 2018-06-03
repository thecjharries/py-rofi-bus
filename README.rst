``py-rofi-bus``
~~~~~~~~~~~~~~~

.. image:: https://badge.fury.io/py/py-rofi-bus.svg
    :target: https://badge.fury.io/py/py-rofi-bus

.. image:: https://travis-ci.org/thecjharries/py-rofi-bus.svg?branch=master
    :target: https://travis-ci.org/thecjharries/py-rofi-bus

.. image:: https://coveralls.io/repos/github/thecjharries/py-rofi-bus/badge.svg?branch=master
    :target: https://coveralls.io/github/thecjharries/py-rofi-bus?branch=master

This package provides a DBus foundation for ``rofi``.

Current version is a proof-of-concept with a simple window switcher. The API will potentially change drastically.



Features
--------

(These are all planned; ``0.2.0`` doesn't expose much of an API)

* Spawn and populate scripts/modi via ``py-rofi-bus``
* Save information from scripts/modi
* Split massive scripts/modi into smaller components that pass state through ``py-rofi-hub``

Setup
------------

System Dependencies
===================

* |rofi_source|_
* XCB Python bindings (preferably |xcffib_source|_)

.. |rofi_source| replace:: The ``rofi`` utility
.. _rofi_source: https://github.com/DaveDavenport/rofi/blob/next/INSTALL.md
.. |xcffib_source| replace:: via ``xcffib``
.. _xcffib_source: https://github.com/tych0/xcffib#installation

Installation
============

.. code:: shell-session

    $ pip install --user py-rofi-bus

Usage
-----

As of ``0.2.0``, logging and help menus are pretty sparse. Expect things to break without a clear reason.

``MainDbusDaemon``
==================

The (current) core of ``py-rofi-bus`` is ``MainDbusDaemon``, which combines all of the important features in some manner with implementing any of them very well. ``MainDbusDaemon`` forks to become a daemon and runs in the background. It publishes a very simple interface to the ``SessionBus`` and waits for interaction from the user. It currently cannot resuscitate itself should its main loop be killed or exited.

CLI Interaction
<<<<<<<<<<<<<<<

``py-rofi-bus`` exposes a very simple CLI to manage ``MainDbusDaemon``.

.. code:: shell-session

    $ which py-rofi-bus
    ~/.local/bin/py-rofi-bus
    $ py-rofi-bus daemon -h
    usage: py-rofi-bus daemon [-h] {start,status,stop} ...

    positional arguments:
      {start,status,stop}  Available actions
        start              Start the daemon
        status             Check the status of the daemon
        stop               Stop the daemon

    optional arguments:
      -h, --help           show this help message and exit

The CLI is independent of the daemon so it can be used to restart the daemon.

DBus Interface
<<<<<<<<<<<<<<

``start``
>>>>>>>>>

Starts the daemon. Doesn't actually do anything (except I don't think I'm properly watching the PID file so it actually just restarts the daemon).

``stop``
>>>>>>>>

Stops the daemon. This kills the daemon's process.

``is_running``
>>>>>>>>>>>>>>

``True`` if the daemon is running; ``GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown`` if the daemon is not running.

``load_apps``
>>>>>>>>>>>>>

This is an experimental feature that attempts to run any executable found in the configured application directory. Files must be marked as executable for the script to be able to load them. So far my cursory tests have demonstrated an ability to load and control both simple scripts and more complicated things like daemons. They've also revealed that I should have planned a bit better and will probably face some refactoring soon.

Example App
===========

I updated the proof-of-concept example. It cast some light on the package's deficiencies. Use it with a grain of salt. Many things that are manual now aren't planned to be manual forever.

Initial Setup
<<<<<<<<<<<<<

Assuming you've installed ``py-rofi-bus``, you'll need to create the configuration directory.

.. code:: shell-session

    $ mkdir -p "$XDG_CONFIG_HOME/wotw/py-rofi-bus/{apps-enabled,pids}"

To run the scripts, they must be in the ``load_from`` config directory, which is probably the one above unless you changed things.

.. code:: shell-session

    $ cd path/to/repo/or/package
    $ ls -l examples/rofi-alt-tab
    total 16
    -rw-r--r--. 1 cjharries cjharries 2457 Jun  3 13:06 active_window_monitor_daemon.py
    -rw-r--r--. 1 cjharries cjharries 2231 Jun  3 13:06 dbus_window_daemon.py
    -rw-r--r--. 1 cjharries cjharries 4826 Jun  3 13:06 ordered_window_script.py
    $ chmod u+x examples/rofi-alt-tab/*.py
    $ source <(
        realpath examples/rofi-alt-tab/*.py | \
            awk '{ print "ln -s "$0" /home/cjharries/.config/wotw/py-rofi-bus/apps-enabled"; }' \
        )
    $ ls -l ~/.config/wotw/py-rofi-bus/apps-enabled
    total 12
    lrwxrwxrwx. 1 cjharries cjharries 103 Jun  3 18:00 active_window_monitor_daemon.py -> <snip>/examples/rofi-alt-tab/active_window_monitor_daemon.py
    lrwxrwxrwx. 1 cjharries cjharries  93 Jun  3 18:00 dbus_window_daemon.py -> <snip>/examples/rofi-alt-tab/dbus_window_daemon.py
    lrwxrwxrwx. 1 cjharries cjharries  96 Jun  3 18:00 ordered_window_script.py -> <snip>/examples/rofi-alt-tab/ordered_window_script.py

If you're not comfortable symlinking the files or don't feel like going to the trouble, you can always do a vanilla copy.

Launching the Daemon
<<<<<<<<<<<<<<<<<<<<

Run the following command:

.. code:: shell-session

    $ py-rofi-bus daemon start

Launching the Example
<<<<<<<<<<<<<<<<<<<<<

Once the files are in the ``load_from`` directory and the daemon is running, you'll have to either add another file or pop open a REPL.

.. code:: shell-session

    $ python

    >>> import pydbus
    >>> bus = pydbus.SessionBus()
    >>> loader = bus.get('pro.wizardsoftheweb.pyrofibus.daemon.window_properties')
    >>> loader.load_apps()
    >>> exit()

