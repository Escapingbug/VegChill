


from vegchill.extension import VegChillPlugin, VegChillInitExt, VegChillCmdExt
from vegchill.plugins.arch import arch
class ContextUtilsInitExt(VegChillInitExt):

    dependency = ['vegchill.plugins.arch:arch']

     
    def __init__(self):
        # TODO
        pass
    
    @classmethod
    def context_register(self,*arg):
        """
        Disaply register information
        """
        # if not self._is_running():
        #     return
        # display register info 
        pc = arch.Arch.pc()
        print("[%s]" % "registers".center(78,"-"))

        return
        
    @classmethod
    def context_code(self,*arg):
        pass


    @classmethod
    def context_stack(self,*arg):
        pass


    @classmethod
    def context(self,*arg):
        """
        Disaplay various information of current exection context

        """
        pass
        

    
    @classmethod
    def name(cls):
        return 'util'
    


class Plugin(VegChillPlugin):
    @classmethod
    def init_ext(cls):
        return []

    @classmethod
    def cmd_ext(cls):
        return []

