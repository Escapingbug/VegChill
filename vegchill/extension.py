class VegChillExt(object):
    @classmethod
    def set_vegchill(cls, vegchill):
        cls.vegchill = vegchill


class VegChillInitExt(VegChillExt):
    """VegChill Init Extension, this class will be instantiated when init the instance,
    and init extension can be accessed from main instance like `veg_chill['ext_path']`"""

    @staticmethod
    def name():
        """name of this extension
        With name, one can access via ext_path, which is the module.ext_name.
        """
        return ''


class VegChillCmdExt(VegChillExt):
    """VegChill Command Extension, see also: https://lldb.llvm.org/python-reference.html"""

    def __init__(self, debugger, session_dict):
        pass

    def __call__(self, debugger, command, exe_ctx, result):
        pass

    def get_short_help(self):
        pass

    def get_long_help(self):
        pass

    @staticmethod
    def cmd():
        """gets the extensions command to add to lldb"""
        raise NotImplementedError("cmd not implemented")


class VegChillPlugin(object):
    """VegChill Plugin"""

    @staticmethod
    def init_ext():
        """get the initalize extensions from the plugin
        Returns:
            object: subclass of init extension or list of that
        """
        raise NotImplementedError("init_ext not implemented")

    @staticmethod
    def cmd_ext():
        """get the command extensions from the plugin
        Returns:
            object: subclass of command extension or list of that
        """
        raise NotImplementedError("cmd_ext not implemented")
