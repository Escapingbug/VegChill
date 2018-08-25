"""
Example vegchill internal plugin

In addition to this directory, you also need to import this package to
parent directory's __init__.py file, see that file for further instruction.

"""
import sys
from vegchill.extension import \
        VegChillPlugin, VegChillInitExt, VegChillCmdExt

class ExampleInitExt(VegChillInitExt):
    """example init extension
    """

    # you may need to specify your dependency here, if you want to
    # depend on some functionality of other extensions
    dependency = []

    @staticmethod
    def name():
        """name of this extension

        Name is important for specify dependency or just specify what extension
        to use.
        When refer to an extension, we use import path of that package then name
        of some specific extension in a form like:

            import_path:name

        For example, to refer to this example init extension, we use:

            vegchill.plugin.example:example

        "vegchill.plugin.example" is the import path, the last "example" is the
        name of this extension

        """
        return 'example'


class ExampleCmdExt(VegChillCmdExt):
    """example command extension
    """

    def __init__(self, *args):
        VegChillCmdExt.__init__(self, *args)

    def __call__(self, debugger, command, exe_ctx, result):
        """lldb support

        This function is required by lldb. If not architecture dependent,
        one can always reuse invoke function, which is required by gdb.

        """
        self.invoke(command, True, result=result)

    def invoke(self, argument, from_tty, result=sys.stdout):
        """gdb support

        This function is required by gdb command implementation.

        """
        print('hello, world')

    def get_short_help(self):
        """short help

        provide short help message

        """
        return 'help message'

    def get_long_help(self):
        """long help

        provide long help message

        """
        return 'long help message'

    @staticmethod
    def cmd():
        """command

        The command you would like to use to refer to this implementation.

        """
        return 'example'

    @staticmethod
    def gdb_command_class():
        """gdb command class

        This function is required by gdb implementation. Please refer to gdb
        documentation for more information.
        """
        import gdb
        return gdb.COMMAND_NONE


class Plugin(VegChillPlugin):
    """Example plugin, import this as plugin in __init__.py in this directory
    """

    @staticmethod
    def init_ext():
        return [ExampleInitExt]

    @staticmethod
    def cmd_ext():
        return [ExampleCmdExt]
