from vegchill.extension import VegChillPlugin, VegChillInitExt
import platform

class UtilInitExt(VegChillInitExt):
    """Util functions.
    This could be used to provided the abstraction over gdb or lldb"""

    priority = 0

    def __init__(self):
        pass

    def set_prompt(self, prompt):
        if self.vegchill.debugger_name == 'gdb':
            import gdb
            gdb.prompt_hook = lambda cur_prompt: prompt
        else:
            import lldb
            lldb.debugger.SetPrompt(prompt)

    @staticmethod
    def name():
        return 'util'


class Plugin(VegChillPlugin):
    @staticmethod
    def init_ext():
        return UtilInitExt

    @staticmethod
    def cmd_ext():
        return []
