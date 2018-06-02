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


class ForkUnitTests(DaemonTestCase):

    def setUp(self):
        DaemonTestCase.setUp(self)
        fork_patcher = patch('py_rofi_bus.components.daemon.fork')
        self.mock_fork = fork_patcher.start()
        self.addCleanup(fork_patcher.stop)
        exit_patcher = patch('py_rofi_bus.components.daemon.sys_exit')
        self.mock_exit = exit_patcher.start()
        self.addCleanup(exit_patcher.stop)

    def test_successful_parent(self):
        self.mock_fork.assert_not_called()
        self.mock_exit.assert_not_called()
        self.daemon.fork()
        self.mock_fork.assert_called_once_with()
        self.mock_exit.assert_not_called()

    def test_successful_child(self):
        self.mock_fork.return_value = 10
        self.mock_fork.assert_not_called()
        self.mock_exit.assert_not_called()
        self.daemon.fork()
        self.mock_fork.assert_called_once_with()
        self.mock_exit.assert_called_once_with(0)

    def test_failed_fork(self):
        self.mock_fork.side_effect = OSError
        self.mock_fork.assert_not_called()
        self.mock_exit.assert_not_called()
        self.daemon.fork()
        self.mock_fork.assert_called_once_with()
        self.mock_exit.assert_called_once_with(1)


class DecoupleFromEnvironmentUnitTests(DaemonTestCase):

    @patch('py_rofi_bus.components.daemon.setsid')
    @patch('py_rofi_bus.components.daemon.umask')
    @patch('py_rofi_bus.components.daemon.chdir')
    def test_calls(self, mock_chdir, mock_umask, mock_sets):
        mock_chdir.assert_not_called()
        mock_umask.assert_not_called()
        mock_sets.assert_not_called()
        self.daemon.decouple_from_environment()
        mock_chdir.assert_called_once_with('/')
        mock_umask.assert_called_once_with(0)
        mock_sets.assert_called_once_with()


class RedirectFileDescriptorsUnitTests(DaemonTestCase):

    def setUp(self):
        DaemonTestCase.setUp(self)
        dup2_patcher = patch('py_rofi_bus.components.daemon.dup2')
        self.mock_dup2 = dup2_patcher.start()
        self.addCleanup(dup2_patcher.stop)
        self.mock_stdout_flush = MagicMock()
        self.mock_stderr_flush = MagicMock()
        stdin_patcher = patch('py_rofi_bus.components.daemon.stdin')
        self.mock_stdin = stdin_patcher.start()
        self.addCleanup(stdin_patcher.stop)
        stdout_patcher = patch(
            'py_rofi_bus.components.daemon.stdout',
            return_value=MagicMock(
                flush=self.mock_stdout_flush,
            ),
        )
        self.mock_stdout = stdout_patcher.start()
        self.addCleanup(stdout_patcher.stop)
        stderr_patcher = patch(
            'py_rofi_bus.components.daemon.stderr',
            return_value=MagicMock(
                flush=self.mock_stderr_flush,
            ),
        )
        self.mock_stderr = stderr_patcher.start()
        self.addCleanup(stderr_patcher.stop)

    def test_flush_calls(self):
        self.mock_stdout_flush.assert_not_called()
        self.mock_stderr_flush.assert_not_called()
        self.daemon.redirect_file_descriptors()


class DaemonizeUnitTests(DaemonTestCase):

    @patch.object(Daemon, 'fork')
    @patch.object(Daemon, 'decouple_from_environment')
    @patch.object(Daemon, 'redirect_file_descriptors')
    @patch.object(Daemon, 'write_pid_file')
    def test_calls(self, mock_pid, mock_fd, mock_decouple, mock_fork):
        mock_pid.assert_not_called()
        mock_fd.assert_not_called()
        mock_decouple.assert_not_called()
        mock_fork.assert_not_called()
        self.daemon.daemonize()
        mock_pid.assert_called_once_with()
        mock_fd.assert_called_once()
        mock_decouple.assert_called_once_with()
        mock_fork.assert_called()
