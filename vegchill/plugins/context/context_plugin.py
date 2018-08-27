from vegchill.extension import VegChillPlugin, VegChillInitExt, VegChillCmdExt

class Plugin(VegChillPlugin):
    @staticmethod
    def init_ext():
        return []

    @staticmethod
    def cmd_ext():
        return []
