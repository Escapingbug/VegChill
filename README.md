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

## Notice

1. Please, make each commit COMPLETE. That is to say, please be sure after the commit, vegchill still works, instead of entering some partial initiated or partial working status.
2. Please, make sure doc-string is there. Document is very important. Although currently we are not working heavily on this, but document as you code will make things a lot easier later.
3. Please, be sure to have a test not long after you adding some new features. Tests are very important to make sure your features are working. At least, test locally manually...But still, I strongly recommand you write some testcase, simplest testcase is OK. I did heavy job to make write testcases easier, please don't fail me.
