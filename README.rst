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

(These are all planned; ``0.1.0`` doesn't expose much of an API)

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

Example
-------

Overview
==========

Because ``0.0.0`` is a POC, I didn't provide ``entry_points``, a robust CLI, unit files, or tests.

This demo was written to emulate ``alt+tab`` functionality on ``i3``, which does not have the notion of "last used window."

The following instructions assume you installed to the user site. If you didn't (e.g. you're in a virtualenv and don't need to), this command will get your package library instead.

.. code::

    python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())"

The DBus Server
===============

The DBus server sets up the communication hub. It can be launched via

.. code::

    $ python "$(python -m site --user-site)/py_rofi_bus/dbus_server.py"

This process provides functions to track the active window, get a list of active windows, and switch to a specified window.

The Window Listener
===================

The window listener sets up the XCB event monitoring. It can be launched via

.. code::

    $ python "$(python -m site --user-site)/py_rofi_bus/window_listener.py"

As before, it must remain active. It monitors the screen's root window for changes in the active window, and reports those changes to the dbus server.

Rofi Window Replacement
=======================

With those two components in place, it's possible to launch the provided modi.

.. code::

    $ chmod +x "$(python -m site --user-site)/py_rofi_bus/rofi_window_script.py"
    $ rofi -modi window_example:"$(python -m site --user-site)/py_rofi_bus/rofi_window_script.py" -show window_example

This modi is almost identical to the stock ``window`` modi. However, using the dbus server, it sorts the windows by activity. When a window is activated, it's pushed to the top of the stack.
