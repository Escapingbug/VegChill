import importlib
import os
from appdirs import user_data_dir

APP_NAME = 'VegChill'
APP_AUTHOR = 'Anciety'

CONFIG_DEFULAT_PATH = os.path.join(user_data_dir(APP_NAME, APP_AUTHOR), 'config')

class VegChill(object):
    """VegChill Main Class
    """

    def __init__(self, config):
        """inits the `VegChill` Class, mainly covers what an extension might need
        Args:
            config (object): a `ConfigParser` object
        """
        self.init_exts = {}
        self.cmd_ext_class = {}
        self.verbose = config.get('option', 'verbose')
        for plugin_import_path in config.options('plugin'):
            module = importlib.import_module(plugin_import_path)
            try:
                plugin = module.plugin
                exts = plugin.init_ext()
                if type(exts) != list:
                    exts = [exts]

                for ext in exts:
                    # all new init extension create
                    self.init_exts['%s.%s' % (plugin_import_path, ext.name())] = ext()

                exts = plugin.cmd_ext()
                if type(exts) != list:
                    exts = [exts]

                for ext in exts:
                    if self.cmd_ext_class.get(ext.cmd()):
                        print('Warning: command %s already exists! Rewritten' % ext.cmd())
                    self.cmd_ext_class[ext.cmd()] = ext
            except AttributeError as e:
                print('Plugin %s load fail, ignored.' % plugin_import_path)
                if self.verbose == 'true':
                    print('Error reason:')
                    print(e)

def lldb_init_module(debugger, internal_dict, config_path=CONFIG_DEFULAT_PATH):
    import lldb
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.read(config_path)

    # add default modules
    import pkgutil
    for _, plugin_name, _ in pkgutil.iter_modules(['vegchill/plugins']):
        config.set('plugin', 'vegchill.plugins.%s' % plugin_name)

    vegchill = VegChill(config)

    # add commands
    has_imported = False
    for cmd_name in vegchill.cmd_ext_class:
        if not has_imported:
            lldb.debugger.HandleCommand('command script import vegchill')
            has_imported = True
        cmd_ext = vegchill.cmd_ext_class[cmd_name]
        module_path = '%s.%s' % (cmd_ext.__module__, cmd_ext.__name__)
        cmd = 'command script add -c %s %s' % (module_path, cmd_name)
        lldb.debugger.HandleCommand(cmd)
