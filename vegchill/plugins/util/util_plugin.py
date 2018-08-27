from vegchill.extension import VegChillPlugin, VegChillInitExt
from .mapping import MemoryMappings
from .file_util import *
import platform

class UtilInitExt(VegChillInitExt):
    """Util functions.
    This could be used to provided the abstraction over gdb or lldb"""

    def __init__(self):
        self.is_gdb = self.vegchill.environ['debugger'] == 'gdb'

    def set_prompt(self, prompt):
        # type: (str)
        """sets prompt

        Args:
            prompt: prompt text

        """
        if self.is_gdb:
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
        
    def pid(self):
        """gets current debuggee pid
        """
        if self.is_gdb:
            return gdb_get_pid()
        else:
            raise NotImplemented('lldb pid function not implemented')

    def file_path(self):
        """gets current debuggee file path
        """
        if self.is_gdb:
            return gdb_get_file_path(self.vegchill)
        else:
            raise NotImplemented('lldb file_path function not implemented')

    def is_remote(self):
        """checks if current debug session is to debug remote file
        """
        if self.is_gdb:
            return gdb_is_remote()
        else:
            raise NotImplemented('lldb is_remote not implemented')

    @classmethod
    def name(cls):
        return 'util'


class Plugin(VegChillPlugin):
    @staticmethod
    def init_ext():
        return UtilInitExt

    @staticmethod
    def cmd_ext():
        return []
