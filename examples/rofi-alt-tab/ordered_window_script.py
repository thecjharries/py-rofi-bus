#!/usr/bin/env python
# pylint:disable=W,C,R

from re import compile as re_compile, finditer, search
from subprocess import PIPE, Popen
from sys import exit as sys_exit

from pydbus import SessionBus
from xpybutil.ewmh import get_desktop_names, get_wm_desktop, get_wm_name
from xpybutil.util import get_property


from py_rofi_bus.components import Script

# https://github.com/DaveDavenport/rofi/blob/next/doc/rofi.1.markdown#window-switcher-settings
WINDOW_FORMAT_PATTERN = re_compile(
    r'(?:/\*)?\s*window-format\s*:\s*(?P<window_format>[\s\S]*?)?\s*;\s*(?:\*/)?',
)

# man rofi | awk '/-window-format format/{ on = 1; } \
#                 /-window-command cmd/{ on = 0; exit; } \
#                 on { print $0; }'
DEFAULT_WINDOW_FORMAT = '{w} {c} {t}'

DESKTOP_NAMES = get_desktop_names().reply()


class OrderedWindowScript(Script):

    MAP_FORMAT_TO_CALLBACK = {
        'w': 'get_rofi_desktop_name',
        't': 'get_rofi_window_title',
        'n': 'get_rofi_window_name',
        'r': 'get_rofi_window_role',
        'c': 'get_rofi_window_class',
    }

    def __init__(self, *args, **kwargs):
        self.bus = SessionBus()
        self.remote = self.bus.get(
            'pro.wizardsoftheweb.pyrofibus.daemon.window_properties')
        self.result = None
        self.row_order = []
        self.format_string = ''
        self.max = []
        self.items = []

    def parse_args(self, process_args=None):
        if process_args and process_args[0]:
            self.result = int(process_args[0].strip().split(' ')[-1])

    def loop_callback(self):
        if self.result:
            self.remote.activate_window(self.result)
            sys_exit(0)

    @staticmethod
    def dump_config():
        result, _ = Popen(['rofi', '-dump-config'], stdout=PIPE).communicate()
        return result.strip()

    @staticmethod
    def discover_window_format(rofi_config):
        possible = search(
            WINDOW_FORMAT_PATTERN,
            rofi_config,
        )
        if possible and possible.group('window_format'):
            return possible.group('window_format').strip()
        return DEFAULT_WINDOW_FORMAT

    @staticmethod
    def get_rofi_desktop_name(window_id):
        return DESKTOP_NAMES[get_wm_desktop(window_id).reply()]

    @staticmethod
    def get_rofi_window_title(window_id):
        return get_wm_name(window_id).reply().encode('utf-8')

    @staticmethod
    def get_rofi_window_role(window_id):
        return get_property(window_id, 'WM_WINDOW_ROLE')\
            .reply()\
            .value\
            .to_string()

    @staticmethod
    def get_rofi_window_class(window_id):
        return get_property(window_id, 'WM_CLASS')\
            .reply()\
            .value\
            .to_string()\
            .split('\x00')[1]

    @staticmethod
    def get_rofi_window_name(window_id):
        return get_property(window_id, 'WM_CLASS')\
            .reply()\
            .value\
            .to_string()\
            .split('\x00')[0]

    @staticmethod
    def convert_format_to_callbacks(window_format):
        row_order = []
        for discovery in finditer(r'(?P<field>[wtnrc])', window_format):
            if discovery and discovery.group('field'):
                letter = discovery.group('field')
                key = OrderedWindowScript.MAP_FORMAT_TO_CALLBACK[letter]
                row_order.append(getattr(OrderedWindowScript, key))
        row_order.append(lambda x: str(x))
        return row_order, [0 for _ in row_order]

    def get_single_window(self, window_id):
        new_item = [callback(window_id) for callback in self.row_order]
        new_max = []
        for new_entry, old_max in zip(new_item, self.max):
            new_length = len(new_entry)
            new_max.append(
                new_length
                if new_length > old_max
                else old_max
            )
        self.max = new_max
        return new_item

    def get_all_windows(self):
        items = []
        for window_id in self.remote.get_window_list():
            items.append(self.get_single_window(window_id))
        return items

    def construct_output(self):
        rofi_config = self.dump_config()
        window_format = self.discover_window_format(rofi_config)
        self.row_order, self.max = self.convert_format_to_callbacks(
            window_format)
        self.items = self.get_all_windows()
        self.items.append(self.items.pop(0))

    def format_output(self):
        self.format_string = ''
        for peak in self.max:
            self.format_string += ' {' + ':' + str(peak) + '} '
        self.format_string = self.format_string.strip()

    def dump_output(self):
        for item in self.items:
            print(self.format_string.format(*item))


if '__main__' == __name__:
    OrderedWindowScript.bootstrap()
