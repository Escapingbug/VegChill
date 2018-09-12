import unittest
import vegchill.vegchill
import subprocess

veg = vegchill.vegchill.veg

class TestMappingUtil(unittest.TestCase):

    def setUp(self):
        self.process = subprocess.Popen(
            'cat',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

    def tearDown(self):
        self.process.kill()

    def test_read_mapping(self):
        util = veg.init_exts['vegchill.plugins.util:util']
        process = self.process
        # FIXME how about windows?
        pid = process.pid
        self.assertIsNotNone(util.read_mapping_unix(pid))
        # TODO more tests on mapping
