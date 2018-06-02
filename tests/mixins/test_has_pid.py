# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus.components.mixins import HasPid


class HasPidTestCase(TestCase):

    def setUp(self):
        self.construct_has_pid()
        self.addCleanup(self.wipe_has_pid)

    def wipe_has_pid(self):
        del self.has_pid

    def construct_has_pid(self):
        self.mock_pid = MagicMock()
        hasconfig_patcher = patch(
            'py_rofi_bus.components.mixins.has_pid.HasConfig.__init__',
            self.mock_pid,
        )
        self.mock_hasconfig = hasconfig_patcher.start()
        self.addCleanup(hasconfig_patcher.stop)
        clear_patcher = patch.object(HasPid, 'clear_pid_file')
        self.mock_clear = clear_patcher.start()
        set_patcher = patch.object(HasPid, 'set_pid_name')
        self.mock_set = set_patcher.start()
        self.has_pid = HasPid()
        clear_patcher.stop()
        set_patcher.stop()
        # self.has_pid.config = {}


class ConstructorUnitTests(HasPidTestCase):

    def test_call(self):
        self.mock_pid.assert_called_once()
        self.mock_clear.assert_called_once()
        self.mock_set.assert_called_once()

    @patch.object(HasPid, 'set_pid_name')
    @patch.object(HasPid, 'clear_pid_file')
    def test_call_branches(self, mock_clear, mock_set):
        has_pid = HasPid('nope')
        self.mock_pid.assert_called()
        self.mock_clear.assert_called()
        self.mock_set.assert_called()
