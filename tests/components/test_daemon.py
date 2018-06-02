# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus.components import Daemon


class DaemonTestCase(TestCase):

    def setUp(self):
        self.construct_daemon()
        self.addCleanup(self.wipe_daemon)

    def wipe_daemon(self):
        del self.daemon

    def construct_daemon(self):
        self.daemon = Daemon()


class IsRunningUnitTests(DaemonTestCase):

    def test_true_with_self(self):
        self.assertTrue(self.daemon.is_running())


class BootstrapUnitTests(DaemonTestCase):

    def setUp(self):
        DaemonTestCase.setUp(self)
        self.mock_run = MagicMock()
        self.mock_quit = MagicMock()
        self.mock_loop = MagicMock(
            MainLoop=MagicMock(
                return_value=MagicMock(
                    run=self.mock_run,
                    quit=self.mock_quit,
                ),
            ),
        )
        glib_patcher = patch(
            'py_rofi_bus.components.daemon.GLib',
            self.mock_loop,
        )
        self.mock_glib = glib_patcher.start()
        self.addCleanup(glib_patcher.stop)
        bus_patcher = patch('py_rofi_bus.components.daemon.SessionBus')
        self.mock_bus = bus_patcher.start()
        self.addCleanup(bus_patcher.stop)

    def test_publish_call(self):
        bootstrap = Daemon.bootstrap
        mock_daemon = patch('py_rofi_bus.components.daemon.Daemon').start()
        mock_daemon.assert_not_called()
        bootstrap()
        mock_daemon.assert_called_once_with()

    def test_try_except(self):
        self.mock_run.side_effect = KeyboardInterrupt
        self.mock_loop.assert_not_called()
        self.mock_run.assert_not_called()
        self.mock_quit.assert_not_called()
        Daemon.bootstrap()
        self.mock_run.assert_called_once_with()
        self.mock_quit.assert_called_once_with()
