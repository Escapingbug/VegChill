from vegchill.extension import VegChillCmdExt, VegChillPlugin
import commands
import platform

class LsCmdExt(VegChillCmdExt):
    """ls-like functionality
    """
    def __init__(self, debugger, session_dict):
        pass

    def __call__(self, debugger, command, exe_ctx, result):
        if platform.system() != 'windows':
            print >>result, (commands.getoutput('ls %s' % command))
        else:
            print >>result, (commands.getoutput('dir %s' % command))

    def get_short_help(self):
        return 'list current directory'

    def get_long_help(self):
        return 'list current directory files'

    @staticmethod
    def cmd():
        return 'ls'


class Plugin(VegChillPlugin):
    
    @staticmethod
    def init_ext():
        return []

    @staticmethod
    def cmd_ext():
        return LsCmdExt
