class VegChillExt(object):
    dependency = []

    @classmethod
    def set_vegchill(cls, vegchill):
        cls.vegchill = vegchill

    @staticmethod
    def gdb_support():
        """is this extension support gdb or not"""
        return True

    @staticmethod
    def lldb_support():
        """is this extension support lldb or not"""
        return True

try:
    import gdb
    Command = gdb.Command
except:
    Command = object

class VegChillInitExt(VegChillExt):
    """VegChill Init Extension, this class will be instantiated when init the instance,
    and init extension can be accessed from main instance like `veg_chill['ext_path']`"""

    @staticmethod
    def name():
        """name of this extension
        With name, one can access via ext_path, which is written as module:ext_name.
        """
        return ''


class VegChillCmdExt(VegChillExt, Command):
    """VegChill Command Extension, see also: https://lldb.llvm.org/python-reference.html"""

    def __init__(self, *args):
        """lldb and gdb supported initialize
        When in context of lldb, function args:
            def __init__(self, debugger, session_dict):
        or gdb:
            def __init__(self, name, command_class)
        but in gdb you don't need to do anything, just use parent's init function
        """
        if self.vegchill.environ['debugger'] == 'gdb':
            Command.__init__(self, *args)

    def __call__(self, debugger, command, exe_ctx, result):
        """lldb call function"""
        raise NotImplementedError('command extension __call__ must be implemented')

    def invoke(self, argument, from_tty):
        """gdb's invoke function"""
        raise NotImplementedError('gdb invoke not implemented')

    def get_short_help(self):
        pass

    def get_long_help(self):
        pass

    @staticmethod
    def cmd():
        """gets the extensions command to add to lldb"""
        raise NotImplementedError("cmd not implemented")

    @staticmethod
    def gdb_cmd_class():
        """if this command supports gdb as well, this will give out its command class.
        see: https://sourceware.org/gdb/onlinedocs/gdb/Commands-In-Python.html
        If not, returns None.
        """
        return None

    
class VegChillPlugin(object):
    """VegChill Plugin"""

    @staticmethod
    def init_ext():
        """get the initalize extensions from the plugin
        Returns:
            object: subclass of init extension or list of that
        """
        raise NotImplementedError("init_ext not implemented")

    @staticmethod
    def cmd_ext():
        """get the command extensions from the plugin
        Returns:
            object: subclass of command extension or list of that
        """
        raise NotImplementedError("cmd_ext not implemented")
