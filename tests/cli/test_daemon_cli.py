# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus.cli import Daemon


class DaemonTestCase(TestCase):

    def setUp(self):
        self.construct_daemon()
        self.addCleanup(self.wipe_daemon)

    def wipe_daemon(self):
        del self.daemon

    def construct_daemon(self):
        parser_patcher = patch('py_rofi_bus.cli.daemon.ArgumentParser')
        self.mock_parser = parser_patcher.start()
        self.addCleanup(parser_patcher.stop)
        self.daemon = Daemon()


class ConstructorUnitTests(DaemonTestCase):

    def test_vanilla(self):
        self.mock_parser.assert_called_once()

    def test_parent_parser(self):
        PARSER = MagicMock()
        PARENT = MagicMock(
            add_parser=PARSER,
        )
        PARSER.assert_not_called()
        Daemon(parent_parser=PARENT)
        PARSER.assert_called_once()


class AttachSubparsersUnitTests(DaemonTestCase):

    def test_call(self):
        SUB = MagicMock()
        self.daemon.parser = MagicMock(
            add_subparsers=SUB,
        )
        SUB.assert_not_called()
        self.daemon.attach_subparsers()
        SUB.assert_called_once()


class AddActionStartUnitTests(DaemonTestCase):

    @patch('py_rofi_bus.cli.daemon.Daemon')
    def test_call(self, mock_daemon):
        PARSER = MagicMock()
        self.daemon.subparsers = MagicMock(
            add_parser=PARSER,
        )
        PARSER.assert_not_called()
        self.daemon.add_action_start()
        PARSER.assert_called_once()


class AddActionStopUnitTests(DaemonTestCase):

    @patch('py_rofi_bus.cli.daemon.Daemon')
    def test_call(self, mock_daemon):
        PARSER = MagicMock()
        self.daemon.subparsers = MagicMock(
            add_parser=PARSER,
        )
        PARSER.assert_not_called()
        self.daemon.add_action_stop()
        PARSER.assert_called_once()


class AddActionStatusUnitTests(DaemonTestCase):

    @patch('py_rofi_bus.cli.daemon.Daemon')
    def test_call(self, mock_daemon):
        PARSER = MagicMock()
        self.daemon.subparsers = MagicMock(
            add_parser=PARSER,
        )
        PARSER.assert_not_called()
        self.daemon.add_action_status()
        PARSER.assert_called_once()


class BootstrapUnitTests(DaemonTestCase):

    @patch('py_rofi_bus.cli.daemon.Application')
    def test_call(self, mock_app):
        mock_app.assert_not_called()
        self.daemon.bootstrap()
        mock_app.assert_called_once_with()

    @patch('py_rofi_bus.cli.daemon.Daemon')
    @patch('py_rofi_bus.cli.daemon.Application')
    def test_daemon_call(self, mock_app, mock_daemon):
        mock_parse = MagicMock(
            return_value=MagicMock(
                subcommand='daemon'
            ),
        )
        mock_app.return_value = MagicMock(
            parser=MagicMock(
                parse_args=mock_parse,
            ),
        )
        mock_app.assert_not_called()
        self.daemon.bootstrap()
        mock_app.assert_called_once_with()
