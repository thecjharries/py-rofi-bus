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
            'py_rofi_bus.components.has_pid.HasConfig.__init__',
            self.mock_pid,
        )
        self.mock_hasconfig = hasconfig_patcher.start()
        self.addCleanup(hasconfig_patcher.stop)
        self.has_pid = HasPid()
