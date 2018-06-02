# pylint:disable=W,C,R
from py_rofi_bus.components import Config


class HasConfig(object):

    def __init__(self, config=None, *args,  **kwargs):
        if isinstance(config, Config):
            self.config = config
        else:
            self.config = Config()
