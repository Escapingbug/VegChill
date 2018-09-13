


from vegchill.extension import VegChillPlugin, VegChillInitExt, VegChillCmdExt
from .context import *
from vegchill.plugins.theme import *



# info = default_theme_plugin.EightColorInitExt()
class ContextUtilsInitExt(VegChillInitExt):

    dependency = ['vegchill.plugins.arch:arch']

    print(dependency)
    def __init__(self):
        self.context_register()

    @staticmethod
    def context_register():
        """
        Display register information of current execution context
        """
  
        print(blue("[%s]" % "registers".center(78,'-')))


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

