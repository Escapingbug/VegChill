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

class RmCmdExt(VegChillCmdExt):
    """Rm-like functionality
    """
    def __init__(self, *args):
        VegChillCmdExt.__init__(self, *args)

    def __call__(self, debugger, command, exe_ctx, result):
        """lldb support"""
        self.invoke(command, True, result=result)
        
    def invoke(self, argument, from_tty, result=sys.stdout):
        """gdb support"""
        output = ""
        if platform.system() != 'windows':
            output = getoutput('rm %s' % argument)
        else:
            output = getoutput('DEL %s' % argument)
        if len(output) > 0:
            six.print_(output , file = result)

    def get_short_help(self):
        return "remove files"


    def get_long_help(self):
        if platform.system() != 'windows':
           return getoutput('rm --help')
        else:
           return getoutput('DEL /?')


    @classmethod
    def cmd(cls):
        return 'rm'

    @classmethod
    def gdb_command_class(cls):
        import gdb
        return gdb.COMMAND_NONE

class MvCmdExt(VegChillCmdExt):
    """Mv-like functionality
    """
    def __init__(self, *args):
        VegChillCmdExt.__init__(self, *args)

    def __call__(self, debugger, command, exe_ctx, result):
        """lldb support"""
        self.invoke(command, True, result=result)
        
    def invoke(self, argument, from_tty, result=sys.stdout):
        """gdb support"""
        output = ""
        if platform.system() != 'windows':
            output = getoutput('mv %s' % argument)
        else:
            output = getoutput('MOVE %s' % argument)
        if len(output) > 0:
            six.print_(output , file = result)

    def get_short_help(self):
        return "move src to dest"

    def get_long_help(self):
        if platform.system() != 'windows':
            return getoutput('mv --help')
        else:
            return getoutput('MOVE /?')

    @classmethod
    def cmd(cls):
        return 'mv'

    @classmethod
    def gdb_command_class(cls):
        import gdb
        return gdb.COMMAND_NONE

class CpCmdExt(VegChillCmdExt):
    """Cp-like functionality
    """
    def __init__(self, *args):
        VegChillCmdExt.__init__(self, *args)

    def __call__(self, debugger, command, exe_ctx, result):
        """lldb support"""
        self.invoke(command, True, result=result)
        
    def invoke(self, argument, from_tty, result=sys.stdout):
        """gdb support"""
        output = ""
        if platform.system() != 'windows':
            output = getoutput('cp %s' % argument)
        else:
            output = getoutput('COPY %s' % argument)
        if len(output) > 0:
            six.print_(output , file = result)

    def get_short_help(self):
        return "copy src to dest"

    def get_long_help(self):
        if platform.system() != 'windows':
           return getoutput('cp --help')
        else:
           return getoutput('COPY /?')

    @classmethod
    def cmd(cls):
        return 'cp'

    @classmethod
    def gdb_command_class(cls):
        import gdb
        return gdb.COMMAND_NONE

class RmdirCmdExt(VegChillCmdExt):
    """Rmdir-like functionality
    """
    def __init__(self, *args):
        VegChillCmdExt.__init__(self, *args)

    def __call__(self, debugger, command, exe_ctx, result):
        """lldb support"""
        self.invoke(command, True, result=result)
        
    def invoke(self, argument, from_tty, result=sys.stdout):
        """gdb support"""
        output = ""
        if platform.system() != 'windows':
            output = getoutput('rmdir %s' % argument)
        else:
            output = getoutput('RD %s' % argument)
        if len(output) > 0 :
            six.print_(output , file = result)

    def get_short_help(self):
        return 'rmdir [OPTION]... DIRECTORY...'


    def get_long_help(self):
        if platform.system() != 'windows':
           return getoutput('rmdir --help')
        else:
           return getoutput('rd [/S] [/Q] [drive:]path') 

    @classmethod
    def cmd(cls):
        return 'rmdir'

    @classmethod
    def gdb_command_class(cls):
        import gdb
        return gdb.COMMAND_NONE

class MkdirCmdExt(VegChillCmdExt):
    """Mkdir-like functionality
    """
    def __init__(self, *args):
        VegChillCmdExt.__init__(self, *args)

    def __call__(self, debugger, command, exe_ctx, result):
        """lldb support"""
        self.invoke(command, True, result=result)
        
    def invoke(self, argument, from_tty, result=sys.stdout):
        """gdb support"""
        output = ""
        if platform.system() != 'windows':
            output = getoutput('mkdir %s' % argument)
        else:
            output = getoutput('MKDIR %s' % argument)
        if len(output) > 0:
            six.print_(output , file = result)

    def get_short_help(self):
        return "create directory(ies)"
        
    def get_long_help(self):
        if platform.system() != 'windows':
           return getoutput('mkdir --help')
        else:
           return getoutput('MKDIR /?') 

    @classmethod
    def cmd(cls):
        return 'mkdir'

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
        return [LsCmdExt , RmCmdExt , RmdirCmdExt , MkdirCmdExt , MvCmdExt , CpCmdExt]
