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
        mock_join.assert_not_called()
        self.has_pid.get_pid_file_name()
        mock_join.assert_called_once()


class ClearPidFileUnitTests(HasPidTestCase):

    def setUp(self):
        HasPidTestCase.setUp(self)
        get_pid_patcher = patch.object(HasPid, 'get_pid_file_name')
        self.mock_get_pid = get_pid_patcher.start()
        self.addCleanup(get_pid_patcher.stop)
        exists_patcher = patch('py_rofi_bus.components.mixins.has_pid.exists')
        self.mock_exists = exists_patcher.start()
        self.addCleanup(exists_patcher.stop)
        kill_patcher = patch('py_rofi_bus.components.mixins.has_pid.kill')
        self.mock_kill = kill_patcher.start()
        self.addCleanup(kill_patcher.stop)
        remove_patcher = patch('py_rofi_bus.components.mixins.has_pid.remove')
        self.mock_remove = remove_patcher.start()
        self.addCleanup(remove_patcher.stop)
        open_patcher = patch('py_rofi_bus.components.mixins.has_pid.open')
        self.mock_open = open_patcher.start()
        self.addCleanup(open_patcher.stop)

    def test_doesnt_exist(self):
        self.mock_exists.return_value = False
        self.mock_exists.assert_not_called()
        self.mock_kill.assert_not_called()
        self.mock_remove.assert_not_called()
        self.mock_open.assert_not_called()
        self.has_pid.clear_pid_file()
        self.mock_exists.assert_called_once()
        self.mock_kill.assert_not_called()
        self.mock_remove.assert_not_called()
        self.mock_open.assert_not_called()

    def test_file_opens(self):
        self.mock_exists.return_value = True
        self.mock_open.return_value = MagicMock()
        self.mock_exists.assert_not_called()
        self.mock_kill.assert_not_called()
        self.mock_remove.assert_not_called()
        self.mock_open.assert_not_called()
        self.has_pid.clear_pid_file()
        self.mock_exists.assert_called_once()
        self.mock_kill.assert_called_once()
        self.mock_remove.assert_called_once()
        self.mock_open.assert_called_once()

    def test_cant_kill(self):
        self.mock_exists.return_value = True
        self.mock_open.return_value = MagicMock()
        self.mock_kill.side_effect = OSError
        self.mock_exists.assert_not_called()
        self.mock_kill.assert_not_called()
        self.mock_remove.assert_not_called()
        self.mock_open.assert_not_called()
        self.has_pid.clear_pid_file()
        self.mock_exists.assert_called_once()
        self.mock_kill.assert_called_once()
        self.mock_remove.assert_called_once()
        self.mock_open.assert_called_once()


class WritePidFileUnitTests(HasPidTestCase):

    @patch('py_rofi_bus.components.mixins.has_pid.open')
    @patch.object(HasPid, 'get_pid_file_name')
    @patch('py_rofi_bus.components.mixins.has_pid.getpid')
    def test_call(self, mock_pid, mock_get, mock_open):
        mock_open.return_value = MagicMock()
        mock_pid.assert_not_called()
        mock_get.assert_not_called()
        self.has_pid.write_pid_file()
        mock_pid.assert_called_once()
        mock_get.assert_called_once()
