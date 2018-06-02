# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus.cli import Application


class ApplicationTestCase(TestCase):

    def setUp(self):
        self.construct_app()
        self.addCleanup(self.wipe_app)

    def wipe_app(self):
        del self.app

    def construct_app(self):
        parser_patcher = patch('py_rofi_bus.cli.application.ArgumentParser')
        self.mock_parser = parser_patcher.start()
        self.addCleanup(parser_patcher.stop)
        self.app = Application()


class ConstructorUnitTests(ApplicationTestCase):

    def test_vanilla(self):
        self.mock_parser.assert_called_once()

    def test_parent_parser(self):
        PARSER = MagicMock()
        PARENT = MagicMock(
            add_parser=PARSER,
        )
        PARSER.assert_not_called()
        app = Application(parent_parser=PARENT)
        PARSER.assert_called_once()


class AttachSubparsersUnitTests(ApplicationTestCase):

    def test_call(self):
        SUB = MagicMock()
        self.app.parser = MagicMock(
            add_subparsers=SUB,
        )
        SUB.assert_not_called()
        self.app.attach_subparsers()
        SUB.assert_called_once()
