# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus.components import Daemon
from py_rofi_bus.components.mixins import HasPid


class DaemonTestCase(TestCase):

    def setUp(self):
        self.construct_daemon()
        self.addCleanup(self.wipe_daemon)

    def wipe_daemon(self):
        del self.daemon

    def construct_daemon(self):
        self.mock_pid = MagicMock()
        haspid_patcher = patch(
            'py_rofi_bus.components.daemon.HasPid.__init__',
            self.mock_pid,
        )
        self.mock_haspid = haspid_patcher.start()
        self.addCleanup(haspid_patcher.stop)
        self.daemon = Daemon()


class ConstructorUnitTests(DaemonTestCase):

    def test_call(self):
        self.mock_pid.assert_called_once()
