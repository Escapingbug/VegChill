import unittest
import vegchill.vegchill
import subprocess

veg = vegchill.vegchill.veg

class TestArch(unittest.TestCase):
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

        self.arch = veg.init_exts['vegchill.plugins.arch:arch']
        self.util = veg.init_exts['vegchill.plugins.util:util']

    def tearDown(self):
        self.process.kill()

    def test_arch(self):
        self.assertIsNotNone(self.util.file_path())
        self.assertEqual(self.arch.arch().name, 'x86_64')
