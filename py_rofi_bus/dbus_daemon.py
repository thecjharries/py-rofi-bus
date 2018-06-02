# pylint:disable=W,C,R
from py_rofi_bus.components import Daemon as DaemonProcess
from py_rofi_bus.dbus import Daemon as DaemonServer


class DbusDaemon(DaemonProcess):

    def main(self):
        print("child main")
        DaemonServer.bootstrap()

if '__main__' == __name__:
    DbusDaemon.bootstrap()
