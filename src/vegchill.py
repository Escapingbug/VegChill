import importlib

class VegChill(object):
    """VegChill Main Class
    """

    def __init__(self, config):
        """inits the `VegChill` Class, mainly covers what an extension might need
        Args:
            config (object): a `ConfigParser` object
        """
        init_exts = {}
        cmd_ext_class = []
        for plugin_import_path in config['plugin']:
            module = importlib.import_module(plugin_import_path)
            try:
                plugin = module.plugin
                exts = plugin.init_ext()
                if type(exts) != list:
                    exts = [exts]

                for ext in exts:
                    init_exts['%s.%s' % (plugin_import_path, ext.name())] = ext()

                exts = plugin.cmd_ext()
                if type(exts) != list:
                    exts = [exts]

                for ext in exts:
                    if cmd_ext_class[ext.cmd()]:
                        print('Warning: command %s already exists! Rewritten' % ext.cmd())
                    cmd_ext_class[ext.cmd()] = ext
            except AttributeError:
                print('plugin %s load fail, ignored.' % plugin_import_path)
