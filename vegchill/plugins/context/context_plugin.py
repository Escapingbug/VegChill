


from vegchill.extension import VegChillPlugin, VegChillInitExt, VegChillCmdExt
from vegchill.plugins.theme import *
import gdb
import functools

# info = default_theme_plugin.EightColorInitExt()

def is_alive():
    """
    Check if GDB is runing
    Return : PID (Int)
    """
    try:
        return gdb.selected_inferior().pid > 0
    except Exception as e:
        return False

class ContextUtilsInitExt(VegChillInitExt):

    dependency = ['vegchill.plugins.arch:arch']

    print(dependency)
    def __init__(self):
        self.context_register()

    def only_is_gdb_running(f):
        """
        Decorator wrapper to check if GDB is running.
        """
        def wrapper(*args, **kwargs):
            if is_alive():
                return f(*args, **kwargs)
            else:
                print(red("No debugging session active"))
        return wrapper
            

    # @staticmethod
    @only_is_gdb_running
    def context_register():
        """
        Display register information of current execution context
        """

        
        print(blue("[%s]" % "registers".center(78,'-')))
        try:
            gdb.execute("info registers")
            gdb.flush()
            
        except Exception as e:
            print(e)

        # print(red("Happy Hacking"))
        


    @classmethod
    def name(cls):
        return 'context'
    


class Plugin(VegChillPlugin):
    @classmethod
    def init_ext(cls):
        return [ContextUtilsInitExt]

    @classmethod
    def cmd_ext(cls):
        return []

