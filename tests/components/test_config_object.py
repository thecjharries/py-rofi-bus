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
        config_dir_patcher = patch.object(Config, 'config_dir')
        self.mock_config_dir = config_dir_patcher.start()
        self.config = Config()
        set_patcher.stop()
        config_dir_patcher.stop()


class ConstructorUnitTests(ConfigTestCase):

    def test_calls(self):
        self.mock_set.assert_called_once()
        self.mock_mkdirp.assert_called_once()


class ApplyDictToSelfUnitTests(ConfigTestCase):
    FINAL = {
        'one': 'two',
        'three': 'four',
    }
    STARTING = {
        'one': 'five',
        'three': 'six',
    }

    def test_with_dict(self):
        for key, value in list(self.STARTING.items()):
            self.config[key] = value
        self.assertNotEqual(self.config, self.FINAL)
        self.config.apply_dict_to_self(self.FINAL)
        self.assertEqual(self.config, self.FINAL)


class SetWithDefaultsUnitTests(ConfigTestCase):

    @patch.object(Config, 'apply_dict_to_self')
    def test_call(self, mock_apply):
        mock_apply.assert_not_called()
        self.config.set_with_defaults()
        self.assertEqual(mock_apply.call_count, 2)


class ConfigDirUnitTests(ConfigTestCase):

    @patch('py_rofi_bus.components.config.join')
    def test_with_application(self, mock_join):
        self.config['application'] = 'yup'
        mock_join.assert_not_called()
        self.config.config_dir
        mock_join.assert_called_once()

    @patch('py_rofi_bus.components.config.join')
    def test_without_application(self, mock_join):
        mock_join.assert_not_called()
        self.config.config_dir
        mock_join.assert_not_called()
