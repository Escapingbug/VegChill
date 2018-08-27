from vegchill.extension import VegChillPlugin, VegChillInitExt
from .elf import Elf

current_elf_file = None
veg = None

def gdb_new_object_handler(event):
    global current_elf_file
    util = veg.init_exts['vegchill.plugins.util:util']
    file_path = util.file_path()
    if file_path:
        current_elf_file = Elf(veg, file_path)
    else:
        veg.info('File path not found')
        current_elf_file = None

class ElfInitExt(VegChillInitExt):
    """Elf function wrapper initalization extension
    """

    dependency = ['vegchill.plugins.util:util']

    def __init__(self):
        global veg
        veg = self.vegchill
        if self.vegchill.environ['debugger'] == 'gdb':
            import gdb
            gdb.events.new_objfile.connect(gdb_new_object_handler)

    def current_elf(self):
        """returns current elf file
        """
        global current_elf_file
        return current_elf_file

    @classmethod
    def name(self):
        return 'elf'
    

class Plugin(VegChillPlugin):
    @staticmethod
    def init_ext():
        return ElfInitExt

    @staticmethod
    def cmd_ext():
        return []
