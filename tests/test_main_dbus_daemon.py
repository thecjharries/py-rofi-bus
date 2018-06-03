# pylint:disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus import MainDbusDaemon


class MainDbusDaemonTestCase(TestCase):

    def setUp(self):
        self.construct_daemon()
        self.addCleanup(self.wipe_daemon)

    def wipe_daemon(self):
        del self.daemon

    def construct_daemon(self):
        self.daemon = MainDbusDaemon()


class MainUnitTests(MainDbusDaemonTestCase):

    @patch('py_rofi_bus.main_dbus_daemon.DaemonServer.bootstrap')
    def test_bootstrap(self, mock_server):
        mock_server.assert_not_called()
        self.daemon.main()
        mock_server.assert_called_once()
