# pylint:disable=W,C,R

from xpybutil.ewmh import (
    get_client_list,
    get_wm_desktop,
    request_active_window,
    request_current_desktop,
)

from py_rofi_bus.dbus import Daemon


class DbusWindowDaemon(Daemon):
    INTERFACE_NAME = "pro.wizardsoftheweb.pyrofibus.daemon.window_properties"
    dbus = """
    <node>
        <interface name='{}'>
            <method name='is_running'>
                <arg type='b' name='response' direction='out'/>
            </method>
            <method name='start'>
            </method>
            <method name='stop'>
            </method>
            <method name='update_active_window'>
                <arg type='i' name='a' direction='in'/>
            </method>
            <method name='activate_window'>
                <arg type='i' name='a' direction='in'/>
            </method>
            <method name='get_window_list'>
                <arg type='ai' name='response' direction='out'/>
            </method>
        </interface>
    </node>
    """.format(INTERFACE_NAME)

    def __init__(self, *args, **kwargs):
        Daemon.__init__(self, *args, **kwargs)
        # super(DbusWindowDaemon, self).__init__(*args, **kwargs)
        self.window_ids = self.get_all_window_ids()

    @staticmethod
    def get_all_window_ids():
        return get_client_list().reply()

    def update_active_window(self, active_window_id):
        global_window_ids = self.get_all_window_ids()
        if active_window_id in self.window_ids:
            self.window_ids.remove(active_window_id)
        self.window_ids.insert(0, active_window_id)
        current_window_ids = self.window_ids[:]
        for window_id in global_window_ids:
            if window_id in self.window_ids:
                current_window_ids.remove(window_id)
            else:
                self.window_ids.append(window_id)
        for window_id in current_window_ids:
            self.window_ids.remove(window_id)

    @staticmethod
    def activate_window(window_id):
        request_current_desktop(get_wm_desktop(window_id).reply())
        request_active_window(window_id)

    def get_window_list(self):
        return self.window_ids

if '__main__' == __name__:
    DbusWindowDaemon.bootstrap()
