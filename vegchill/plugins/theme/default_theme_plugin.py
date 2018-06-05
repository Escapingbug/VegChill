from vegchill.extension import VegChillPlugin, VegChillInitExt
import platform

class DefaultThemeInitExt(VegChillInitExt):

    def __init__(self):
        import lldb
        prompt_text = 'vegchill> '
        if platform.system() != 'windows':
            # FIXME don't know why ansi color code is not working, fix this
            #prompt = '\001\033[1;32m\002{0:s}\001\033[0m\002'.format(prompt_text)
            lldb.debugger.SetPrompt(prompt_text)
        else:
            lldb.debugger.SetPrompt(prompt_text)
    
    @staticmethod
    def name():
        return 'default_theme_init'


class Plugin(VegChillPlugin):
    @staticmethod
    def init_ext():
        return DefaultThemeInitExt

    @staticmethod
    def cmd_ext():
        return []
