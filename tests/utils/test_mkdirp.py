# pylint: disable=W,C,R

from __future__ import print_function

from collections import OrderedDict
from errno import EEXIST
from unittest import TestCase

from mock import call, MagicMock, patch

from py_rofi_bus.utils import mkdirp


class MkdirpTestCase(TestCase):

    def setUp(self):
        self.construct_patches()

    def construct_patches(self):
        makedirs_patcher = patch('py_rofi_bus.utils.mkdirp_function.makedirs')
        self.mock_makedirs = makedirs_patcher.start()
        self.addCleanup(makedirs_patcher.stop)
        isdir_patcher = patch('py_rofi_bus.utils.mkdirp_function.isdir')
        self.mock_isdir = isdir_patcher.start()
        self.addCleanup(isdir_patcher.stop)


class MkdirpUnitTests(MkdirpTestCase):
    DIR_PATH = '/1/2/3'

    def test_no_directory(self):
        self.mock_makedirs.assert_not_called()
        self.mock_isdir.assert_not_called()
        mkdirp()
        self.mock_makedirs.assert_not_called()
        self.mock_isdir.assert_not_called()

    def test_new_directory(self):
        self.mock_makedirs.assert_not_called()
        self.mock_isdir.assert_not_called()
        mkdirp(self.DIR_PATH)
        self.mock_makedirs.assert_called_once_with(self.DIR_PATH)
        self.mock_isdir.assert_not_called()

    def test_old_directory(self):
        self.mock_makedirs.side_effect = OSError(EEXIST, 'whoops')
        self.mock_isdir.return_value = True
        self.mock_makedirs.assert_not_called()
        self.mock_isdir.assert_not_called()
        mkdirp(self.DIR_PATH)
        self.mock_makedirs.assert_called_once_with(self.DIR_PATH)
        self.mock_isdir.assert_called_once_with(self.DIR_PATH)

    def test_broken_path(self):
        self.mock_makedirs.side_effect = OSError
        self.mock_isdir.return_value = True
        self.mock_makedirs.assert_not_called()
        self.mock_isdir.assert_not_called()
        with self.assertRaises(OSError):
            mkdirp(self.DIR_PATH)
        self.mock_makedirs.assert_called_once_with(self.DIR_PATH)
        self.mock_isdir.assert_not_called()
