# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus.dbus import Daemon


class DaemonTestCase(TestCase):

    def setUp(self):
        self.construct_daemon()
        self.addCleanup(self.wipe_daemon)

    def wipe_daemon(self):
        del self.daemon

    def construct_daemon(self):
        self.mock_run = MagicMock()
        self.mock_quit = MagicMock()
        self.mock_loop = MagicMock(
            return_value=MagicMock(
                run=self.mock_run,
                quit=self.mock_quit,
            ),
        )
        loop_patcher = patch(
            'py_rofi_bus.dbus.daemon.MainLoop',
            # MagicMock,
            self.mock_loop,
        )
        self.mock_loop = loop_patcher.start()
        self.mock_bus = MagicMock()
        self.addCleanup(loop_patcher.stop)
        bus_patcher = patch(
            'py_rofi_bus.dbus.daemon.SessionBus',
            self.mock_bus,
        )
        self.mock_bus = bus_patcher.start()
        self.addCleanup(bus_patcher.stop)
        self.daemon = Daemon()


class ConstructorUnitTests(DaemonTestCase):

    def test_empty_ctor_inputs(self):
        self.mock_loop.assert_called_once_with()
        self.mock_bus.assert_called_once_with()

    def test_filled_ctor_inputs(self):
        BUS = MagicMock()
        LOOP = MagicMock()
        self.mock_loop.reset_mock()
        self.mock_bus.reset_mock()
        self.daemon = Daemon(bus=BUS, loop=LOOP)
        self.assertEqual(BUS, self.daemon.bus)
        self.assertEqual(LOOP, self.daemon.loop)


class StartUnitTests(DaemonTestCase):

    def test_while_running(self):
        self.daemon._is_running = True
        self.mock_run.assert_not_called()
        self.mock_quit.assert_not_called()
        self.daemon.start()
        self.mock_run.assert_not_called()
        self.mock_quit.assert_not_called()

    def test_while_stopped(self):
        self.daemon._is_running = False
        self.mock_run.assert_not_called()
        self.mock_quit.assert_not_called()
        self.daemon.start()
        self.mock_run.assert_called_once_with()
        self.mock_quit.assert_not_called()

    def test_with_interrupt(self):
        self.mock_run.side_effect = KeyboardInterrupt
        self.daemon._is_running = False
        self.mock_run.assert_not_called()
        self.mock_quit.assert_not_called()
        self.daemon.start()
        self.mock_run.assert_called_once_with()
        self.mock_quit.assert_called_once_with()


class IsRunningUnitTests(DaemonTestCase):

    def test_default_self(self):
        self.assertFalse(self.daemon.is_running())


class BootstrapUnitTests(DaemonTestCase):

    def setUp(self):
        DaemonTestCase.setUp(self)

    def test_publish_call(self):
        bootstrap = Daemon.bootstrap
        mock_daemon = patch('py_rofi_bus.dbus.daemon.Daemon').start()
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
