# VegChill - VegChicken's LLDB/GDB plugin
`VegChill` is a fully extensible `Xdb` plugin. By `Xdb` I mean lldb or gdb. It is first designed
to be an lldb plugin, but suddenly it seems to be working under gdb as well. With the concept of
`plugin's plugin` and `extension`, it can be easily extended by just `pip install` some related
plugin.

Currently `VegChill` is still in actively development status, many default features are
still missing, and not recommended to try out for now. Once everything's prepared to use,
we'll upload `VegChill` onto `pypi`, thus make it pip installable and show its muscle.

# Contribution

We currently focus on gdb devs. LLDB PRs are welcomed though.

## Steps (gdb)

1. modify some files, or add some files. (If you add anything, be sure to import things in `__init__.py`)
2. do `python setup.py develop`, there will be a `develop_app` directory
3. enter gdb, do `source develop_app/load_vegchill.py`

And everything is loaded. To test things, you can do this:

4. enter gdb, do `source develop_app/test_vegchill.py`

If you want to add some tests, just enter `tests` directory, add your test (Currently, command tests are in `tests/command`, others are in `tests/framework`, this may change since it is not seems to be well defined), remember to import your test (look at the `__init__.py`). Then do that source in your gdb.
