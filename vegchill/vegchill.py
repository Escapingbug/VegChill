import importlib
import os
from appdirs import user_data_dir

APP_NAME = 'VegChill'
APP_AUTHOR = 'Anciety'

CONFIG_DEFULAT_PATH = os.path.join(user_data_dir(APP_NAME, APP_AUTHOR), 'config')

def depends_resolve(exts_with_import_path):
            """does topology sort to resolve dependencies
            """
            class Vert(object):
                def __init__(self, ext, import_path):
                    self.ext = ext
                    self.import_path = import_path
                    self.prior = ext.priority
                    self.in_cnt = len(ext.dependency)

                def __eq__(self, other):
                    return self.prior == other.prior
                def __lt__(self, other):
                    return self.prior < other.prior
                def __le__(self, other):
                    return self.prior <= other.prior
                def __gt__(self, other):
                    return self.prior > other.prior
                def __ge__(self, other):
                    return self.prior >= other.prior

            class Edge(object):
                def __init__(self, frm, to):
                    self.frm = frm
                    self.to = to
            vert_table = {}
            for ext, import_path in exts_with_import_path:
                vert_table[ext.name()] = Vert(ext, import_path)
            edges = set()
            for ext, import_path in exts_with_import_path:
                # check if all depends can be resolved
                vert = vert_table[ext.name()]
                ignoring = False
                for dep in ext.dependency:
                    if dep not in vert_table:
                        print(
                            'Dependency %s of %s.%s not found, ignored.' % (dep, import_path, ext)
                        )
                        ignoring = True
                        break
                if ignoring:
                    continue
                else:
                    edges |= set(map(lambda x: Edge(vert, vert_table[x]), ext.dependency))

            # topology sort with priority considered
            seq = []
            no_deps = sorted(filter(lambda x: x[1].in_cnt == 0, vert_table.items()))
            while len(vert_table) != len(seq):
                seq += list(map(lambda x: x[1], no_deps))
                edges_associated = filter(lambda x: x.frm in no_deps, edges)
                no_deps = []
                for e in edges_associated:
                    e.to.in_cnt -= 1
                    if e.to.in_cnt == 0:
                        no_deps.append(e.to)
                edges -= set(edges_associated)
                if len(no_deps) == 0 and len(vert_table) != len(seq):
                    print('Unresolvable dependencies, nothing will be loaded')
                    return []
            return map(lambda x: (x.ext, x.import_path), seq)


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

        plugins = []
        # load plugins and extensions, but not instantiate anything until
        # dependency and priority resolve phase.
        init_ext_class = []
        for plugin_import_path in config.options('plugin'):
            try:
                plugin = importlib.import_module(plugin_import_path).plugin
                # load all init extension classes, they will be instantiated
                # after dependency and priority resolve.
                exts = plugin.init_ext()
                if type(exts) != list:
                    exts = [exts]
                # associate classes with import path
                # generates list of (ext_class, import_path) tuples
                init_ext_class += list(map(lambda x: (x, plugin_import_path), exts))

                # cmd extensions don't worry about dependency, as they don't need to
                # be instantiated for now
                exts = plugin.cmd_ext()
                if type(exts) != list:
                    exts = [exts]

                for ext in exts:
                    if self.cmd_ext_class.get(ext.cmd()):
                        print('Warning: command %s already exists! Rewritten' % ext.cmd())
                    ext.set_vegchill(self)
                    self.cmd_ext_class[ext.cmd()] = ext
            except AttributeError as e:
                print('Plugin %s load fail, ignored.' % plugin_import_path)
                if self.verbose == 'true':
                    print(e)

        print('doing depends resolution')
        init_ext_class = depends_resolve(init_ext_class)
        for ext, import_path in init_ext_class:
            path = '%s.%s' % (import_path, ext.name())
            self.init_exts[path] = ext()


def init_vegchill(config_path):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    # this is for adding environ plugin, since it must be prior to any others
    config.add_section('plugin')

    # add default modules
    import pkgutil
    for _, plugin_name, _ in pkgutil.iter_modules(['vegchill/plugins']):
        config.set('plugin', 'vegchill.plugins.%s' % plugin_name)

    config.read(config_path)

    vegchill = VegChill(config)
    return vegchill


def lldb_init_module(debugger, internal_dict, config_path=CONFIG_DEFULAT_PATH):
    import lldb

    vegchill = init_vegchill(config_path)
    
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
