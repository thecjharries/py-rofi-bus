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


class SetPidNameUnitTests(HasPidTestCase):
    FINAL = 'yup'
    STARTING = 'nope'

    def test_already_have_pid(self):
        self.has_pid.config = {'pid_name': self.FINAL}
        self.has_pid.pid_name = self.STARTING
        self.assertNotEqual(self.has_pid.pid_name, self.FINAL)
        self.has_pid.set_pid_name()
        self.assertEqual(self.has_pid.pid_name, self.FINAL)

    def test_passed_in(self):
        self.has_pid.config = {}
        self.has_pid.pid_name = self.STARTING
        self.assertNotEqual(self.has_pid.pid_name, self.FINAL)
        self.has_pid.set_pid_name(self.FINAL)
        self.assertEqual(self.has_pid.pid_name, self.FINAL)

    def test_no_pid_name(self):
        self.has_pid.config = {}
        self.has_pid.pid_name = self.STARTING
        self.assertNotEqual(self.has_pid.pid_name, self.FINAL)
        self.has_pid.set_pid_name()
        self.assertEqual(self.has_pid.pid_name, '')


class GetPidFileNameUnitTests(HasPidTestCase):

    @patch('py_rofi_bus.components.mixins.has_pid.join')
    def test_call(self, mock_join):
        self.has_pid.config = MagicMock()
        self.has_pid.pid_name = 'qqq'
        # setattr(self.has_pid.config, 'config_dir', 'qqq')
        mock_join.assert_not_called()
        self.has_pid.get_pid_file_name()
        mock_join.assert_called_once()
