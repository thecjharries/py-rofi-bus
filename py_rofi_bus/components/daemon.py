# pylint:disable=W,C,R
from pydbus import SessionBus
from gi.repository import GLib


class Daemon(object):
    INTERFACE_NAME = "pro.wizardsoftheweb.pyrofibus.daemon"
    dbus = """
    <node>
        <interface name='{}'>
            <method name='is_running'>
                <arg type='b' name='response' direction='out'/>
            </method>
        </interface>
    </node>
    """.format(INTERFACE_NAME)

    def is_running(self):
        if self:
            return True
        # This should never occur; to be called self must exist
        return False  # pragma: no cover

    @staticmethod
    def bootstrap():
        loop = GLib.MainLoop()
        bus = SessionBus()
        bus.publish(Daemon.INTERFACE_NAME, Daemon())
        try:
            loop.run()
        except KeyboardInterrupt:
            loop.quit()

if '__main__' == __name__:
    Daemon.bootstrap()
