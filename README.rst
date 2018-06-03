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

Usage
-----

As of ``0.2.0``, logging and help menus are pretty sparse. Expect things to break without a clear reason.

``MainDbusDaemon``
==================

The (current) core of ``py-rofi-bus`` is ``MainDbusDaemon``, which combines all of the important features in some manner with implementing any of them very well. ``MainDbusDaemon`` forks to become a daemon and runs in the background. It publishes a very simple interface to the ``SessionBus`` and waits for interaction from the user. It currently cannot resuscitate itself should its main loop be killed or exited.

