import unittest
import vegchill.vegchill
import subprocess

veg = vegchill.vegchill.veg

class TestFileUtil(unittest.TestCase):
    
    def setUp(self):
        self.process = subprocess.Popen(
            'cat',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        try:
            import gdb
            self.is_gdb = True
        except:
            self.is_gdb = False

        if self.is_gdb:
            gdb.execute('attach %d' % self.process.pid)

        self.util = veg.init_exts['vegchill.plugins.util:util']

    
    def tearDown(self):
        self.process.kill()

    
    def test_pid(self):
        process = self.process
        pid = process.pid
        self.assertEqual(self.util.pid(), pid)

    
    def test_is_remote(self):
        self.assertEqual(self.util.is_remote(), False)

    
    def test_file_path(self):
        self.assertIsNotNone(self.util.file_path())
        self.assertEqual(self.util.file_path(), '/usr/bin/cat')
