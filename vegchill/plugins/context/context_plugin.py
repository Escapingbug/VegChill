from vegchill.extension import VegChillPlugin, VegChillInitExt, VegChillCmdExt

class Plugin(VegChillPlugin):
    @classmethod
    def init_ext(cls):
        return []

    @classmethod
    def cmd_ext(cls):
        return []
