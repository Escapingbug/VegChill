from vegchill.extension import VegChillPlugin, VegChillInitExt
from .mapping import MemoryMappings
import platform

class UtilInitExt(VegChillInitExt):
    """Util functions.
    This could be used to provided the abstraction over gdb or lldb"""

    def __init__(self):
        pass

    def set_prompt(self, prompt):
        # type: (str)
        if self.vegchill.environ['debugger'] == 'gdb':
            import gdb
            gdb.prompt_hook = lambda cur_prompt: prompt
        else:
            import lldb
            lldb.debugger.SetPrompt(prompt)

    def read_mapping_unix(self, pid):
        # type: (int) -> MemoryMappings
        """read mapping file and get mapping information

        Args:
            pid: *nix pid of the process

        Returns:
            memory mapping representation
        """
        return MemoryMappings.parse_from_pid(self.vegchill, pid)
        

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
