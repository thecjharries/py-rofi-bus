# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus.components import Config


class ConfigTestCase(TestCase):

    def setUp(self):
        self.construct_config()
        self.addCleanup(self.wipe_config)

    def wipe_config(self):
        del self.config

    def construct_config(self):
        mkdirp_patcher = patch('py_rofi_bus.components.config.mkdirp')
        self.mock_mkdirp = mkdirp_patcher.start()
        self.addCleanup(mkdirp_patcher.stop)
        set_patcher = patch.object(Config, 'set_with_defaults')
        self.mock_set = set_patcher.start()
        self.config = Config()
        set_patcher.stop()
