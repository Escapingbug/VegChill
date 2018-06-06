# VegChill's Extension Framework
VegChill is fully extensible. The design behind that accomplish this is the "Extension Framework".
As VegChill being an lldb plugin, the framework can support "plugin's plugin".

# Under The Hood
Thanks to `Python`'s dynamic features, everything can be dynamically loaded, the framework totally
makes great use of that. 

Framework defines what to be a plugin, and what is a extension. A plugin is a plugin of `VegChill`
instead of lldb, as the plugin to lldb is `VegChill` itself. A plugin consists of extensions. An
extension can be of some extension type. Now we are talking about these features and how it works.

# VegChill
VegChill is the main object which is responsible for global jobs like init all extensions and
provide a scope to save variables.

# Plugin
Note again: here the plugin refers to our plugin, not lldb's. It is basically a lldb's plugin's
plugin.

So, to support plugin, one should export a python name `plugin`, and makes it a subclass of
`VegChillPlugin`, implement what is missing. `VegChillPlugin` looks like this:
```
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

```
There are currently two methods to be implemented, and must be implemented. These two methods
are for `VegChill` to know what functionality your plugin should provide, by using a concept
of extension which we will mention later on.

To implement your plugin, just create your own project, and make sure there is a name called
`plugin` directly exported and has implemented as a subclass of `VegChillPlugin`. Now we will
answer the question about what is extension.

# Extension
An extension is where the magic happens. They are responsible for the internal logic a plugin
should provide. Note that all extension classes have a `.vegchill` variable associated, this
is where we provide `VegChill` object to extensions. One can always use this to find the main
object once it is up(Since extension is initialized once we have a vegchill object already,
this is almost always accessable).

## init extension
Init extensions, also called `InitExt`, is instantiated when the `VegChill` is created. They are
designed to provide extra functions or some features that do their things when the system is up.

For example, to support beautify features, like changing the lldb's prompt, this should be done
once the `VegChill` is up, so we make it a init extension.

Init extension is implemented by subclassing `VegChillInitExt`, futhur documentation will be
provided, or you can read the source code directly(as for now, the documentation site is not done).

Init extension can be acesssed after it is up, by using `VegChill.init_exts['ext_path']`, the
`ext_path` here refers to the module path, like "vegchill.plugins.theme.DefaultThemeInitExt".
Or something like "your_module.init_ext_name". So to provide extra util functions, you can make
it an init extension, and use it later on by using the `VegChill.init_exts`.

## command extension
Command extensions, also called `CmdExt` is to insert new command enhancement into lldb.

For example, we want to add a new command called `ls` and can be used inside lldb to list current
directory, we make it a comamnd extension.

A command extension is done by subclassing the `VegChillCmdExt` and implement what is missing.
Note that the `__init__` and `__call__` must be implemented as for the requirements of lldb.

The model is, if you need something that needs global info, you can use init extension to do that,
and access init info using `VegChill` object.

# Examples
Simple implementation internally can be seen as an example.
Currently the implementation of `vegchill.plugins.theme` can be a good example of a plugin of just
one init extension, and `vegchill.plugins.shell_cmd` can be a good example of a plugin of command
extensions.

But do note that these two are `default extensions`, and they don't need to be exported. For
external plugin examples, please wait till we have done what is default used.
