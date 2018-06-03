# pylint: disable=W,C,R

from __future__ import print_function

from collections import deque
from sys import exit as sys_exit

from pydbus import SessionBus

import xcffib
import xcffib.xproto
from xpybutil.ewmh import get_active_window

from py_rofi_bus.components import Daemon


class ActiveWindowMonitorDaemon(Daemon):

    def __init__(self, *args, **kwargs):
        super(ActiveWindowMonitorDaemon, self).__init__(*args, **kwargs)
        self.event_queue = deque()
        self.set_up_xcffib()

    def set_up_xcffib(self):
        self.connection = xcffib.connect()
        self.root = self.connection.get_setup().roots[0].root
        self.connection.core.ChangeWindowAttributesChecked(
            self.root,
            xcffib.xproto.CW.EventMask,
            [xcffib.xproto.EventMask.PropertyChange],
        ).check()

    def fill_queue(self):
        current_event = self.connection.wait_for_event()
        self.event_queue.appendleft(current_event)
        while True:
            try:
                trailing_event = self.connection.poll_for_event()
                if trailing_event:
                    self.event_queue.appendleft(trailing_event)
                else:
                    break
            except KeyboardInterrupt:
                sys_exit(0)

    @property
    def events(self):
        while len(self.event_queue):
            yield self.event_queue.pop()

    def check_event(self, event):
        atom_name = self.connection.core.\
            GetAtomName(event.atom)\
            .reply()\
            .name\
            .to_string()
        if '_NET_ACTIVE_WINDOW' == atom_name:
            print('cool')

    def drain_queue(self):
        for event in self.events:
            self.check_event(event)

    def main(self):
        while True:
            try:
                self.fill_queue()
                self.drain_queue()
            except KeyboardInterrupt:
                sys_exit(0)

if '__main__' == __name__:
    ActiveWindowMonitorDaemon.bootstrap()
