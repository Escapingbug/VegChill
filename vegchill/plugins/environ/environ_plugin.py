from vegchill.extension import VegChillPlugin, VegChillInitExt
import platform

class EnvironInitExt(VegChillInitExt):
    """Environ extension provide scope for global variables"""

    # highest priority
    priority = 0

    def __init__(self):
        self.env = {
            # gdb to be supported
            'debugger_name': 'lldb'
        }

    def __getitem__(self, key):
        return self.env[key]

    def __setitem__(self, key, val):
        self.env[key] = val
    
    @staticmethod
    def name():
        return 'environ'


class Plugin(VegChillPlugin):
    @staticmethod
    def init_ext():
        return EnvironInitExt

    @staticmethod
    def cmd_ext():
        return []
