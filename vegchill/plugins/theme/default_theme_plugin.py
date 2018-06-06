from vegchill.extension import VegChillPlugin, VegChillInitExt
import platform

class DefaultThemeInitExt(VegChillInitExt):

    dependency = ['vegchill.plugins.util.util']

    def __init__(self):
        util = self.vegchill.init_exts['vegchill.plugins.util.util']
        prompt_text = 'vegchill> '
        if platform.system() != 'windows':
            # FIXME don't know why ansi color code is not working, fix this
            #prompt = '\001\033[1;32m\002{0:s}\001\033[0m\002'.format(prompt_text)
            prompt = prompt_text
            util.set_prompt(prompt)
        else:
            util.set_prompt(prompt_text)
    
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
