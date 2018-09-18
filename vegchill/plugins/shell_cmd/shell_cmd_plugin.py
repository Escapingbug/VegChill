from vegchill.extension import VegChillCmdExt, VegChillPlugin
import platform
import six
from six.moves import getoutput
import sys

class LsCmdExt(VegChillCmdExt):
    """ls-like functionality
    """
    def __init__(self, *args):
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

    @classmethod
    def cmd(cls):
        return 'ls'

    @classmethod
    def gdb_command_class(cls):
        import gdb
        return gdb.COMMAND_NONE


class Plugin(VegChillPlugin):
    
    @classmethod
    def init_ext(cls):
        return []

    @classmethod
    def cmd_ext(cls):
        return LsCmdExt
