"""environment object, saves import status of main object
"""
class Environ(object):

    LOG_LEVEL_TABLE = {
        'debug': 0,
        'info': 1,
        'warn': 2,
        'err': 3,
        'emer': 4,
    }

    def __init__(self):
        self.internal = {}

    def __getitem__(self, name):
        return self.internal[name]

    def __setitem__(self, name, value):
        self.internal[name] = value

    @staticmethod
    def from_config(config):
        """gets environment out of config object

        Args:
            config: config object

        Returns:
            Environ object

        """
        environ = Environ()
        log_level_str = config.get('option', 'log_level').lower()
        environ['log_level'] = Environ.LOG_LEVEL_TABLE[log_level_str]
        return environ
