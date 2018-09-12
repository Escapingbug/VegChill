"""architecture plugin
"""
import operator
from vegchill.extension import VegChillPlugin, VegChillInitExt
from .arch import *

class ArchInitExt(VegChillInitExt):

    dependency = ['vegchill.plugins.elf:elf']

    def __init__(self):
        is_gdb = self.vegchill.environ['debugger'] == 'gdb'
        self.elf_ext = self.vegchill.init_exts['vegchill.plugins.elf:elf']
        ArchInitExt.ARCH_TABLE = {
            'x86': ArchX86(is_gdb),
            'x86_64': ArchX86_64(is_gdb),
        }
        

    def get_arch(self, arch_name):
        # type: (str) -> Arch
        """get architecture object

        Args:
            arch_name: architecture name

        Returns:
            Arch object

        """
        return self.ARCH_TABLE[arch_name]

    def arch(self):
        """returns current architecture object
        """
        current_elf = self.elf_ext.current_elf()
        if current_elf is not None:
            return ArchInitExt.ARCH_TABLE[current_elf.arch_name()]
        else:
            return None

    @classmethod
    def name(cls):
        return 'arch'


class Plugin(VegChillPlugin):
    @classmethod
    def init_ext(cls):
        return ArchInitExt

    @classmethod
    def cmd_ext(cls):
        return []
