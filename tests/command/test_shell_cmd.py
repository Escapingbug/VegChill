import unittest
from six.moves import getoutput 

def test_command(self, command, gdb, lldb):
    if gdb:
        res = gdb.execute(command, from_tty=True, to_string=True)
        self.assertEqual(res, getoutput(command) + '\n')
    else:
        ci = lldb.debugger.GetCommandInterpreter()
        ret = lldb.SBCommandReturnObject()
        ci.HandleCommand(command, ret)
        self.assertEqual(ret.GetOutput(), getoutput(command) + '\n')


class TestShellCommand(unittest.TestCase):
    # TODO test commands with args

    def setUp(self):
        self.gdb = None
        self.lldb = None

        try:
            import gdb
            self.gdb = gdb
        except:
            pass

        try:
            import lldb
            if self.lldb.debugger is None:
                self.lldb = None
            self.lldb = lldb
        except:
            pass

        if self.gdb is None and self.lldb is None:
            raise Exception('no gdb or lldb available')

    
    def test_ls(self):
        test_command(self, 'ls', self.gdb, self.lldb)

    def test_mkdir(self):
        test_command(self, 'mkdir', self.gdb, self.lldb)

    def test_mv(self):
        test_command(self, 'mv', self.gdb, self.lldb)

    def test_cp(self):
        test_command(self, 'cp', self.gdb, self.lldb)

    def test_rm(self):
        test_command(self, 'rm', self.gdb, self.lldb)
