from vegchill.extension import VegChillPlugin, VegChillInitExt, VegChillCmdExt

class ContextUtilsInitExt(VegChillInitExt):

    dependency = ['vegchill.plugins.arch:arch']

    def __init__(self):
        # TODO
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
