Example
-------

*Note*: The paths won't work anymore. You can piece together how it worked if you're really interested. This will be reworked (eventually) with ``py-rofi-bus`` proper.

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
