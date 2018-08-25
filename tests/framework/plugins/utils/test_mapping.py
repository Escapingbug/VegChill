import unittest
import vegchill.vegchill
import subprocess

Veg = vegchill.vegchill.Veg

class TestMappingUtil(unittest.TestCase):
    def test_read_mapping(self):
        util = Veg.init_exts['vegchill.plugins.util:util']
        # FIXME how about windows?
        process = subprocess.Popen(
            'cat',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        pid = process.pid
        self.assertIsNotNone(util.read_mapping_unix(pid))
        # TODO more tests on mapping
        process.kill()
