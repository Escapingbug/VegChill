from vegchill.extension import VegChillCmdExt, VegChillPlugin
import platform
import six
from six.moves import getoutput
import sys

class LsCmdExt(VegChillCmdExt):
    """ls-like functionality
    """
    def __init__(self, *args):
        if self.vegchill.debugger_name == 'gdb':
            VegChillCmdExt.__init__(self, *args)

    def __call__(self, debugger, command, exe_ctx, result):
        """lldb support"""
        self.invoke(command, True, result=result)
        
    def invoke(self, argument, from_tty, result=sys.stdout):
        """gdb support"""
        if platform.system() != 'windows':
            six.print_(getoutput('ls %s' % argument), file=result)
        else:
            six.print_(getoutput('dir %s' % argument), file=result)

    def get_short_help(self):
        return 'list current directory'

    def get_long_help(self):
        return 'list current directory files'

    @staticmethod
    def cmd():
        return 'ls'

    @staticmethod
    def gdb_command_class():
        import gdb
        return gdb.COMMAND_NONE


class Plugin(VegChillPlugin):
    
    @staticmethod
    def init_ext():
        return []

    @staticmethod
    def cmd_ext():
        return LsCmdExt
