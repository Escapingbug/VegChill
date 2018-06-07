import unittest

class TestShellCommand(unittest.TestCase):
    def test_ls(self):
        gdb = None
        lldb = None
        try:
            import gdb
        except:
            pass

        try:
            import lldb
            if lldb.debugger is None:
                lldb = None
        except:
            pass

        if gdb is None and lldb is None:
            raise Exception('no gdb or lldb available')

        from six.moves import getoutput
        if gdb:
            res = gdb.execute('ls', from_tty=True, to_string=True)
            self.assertEqual(res, getoutput('ls') + '\n')
        else:
            ci = lldb.debugger.GetCommandInterpreter()
            ret = lldb.SBCommandReturnObject()
            ci.HandleCommand('ls', ret)
            self.assertEqual(ret.GetOutput(), getoutput('ls') + '\n')
