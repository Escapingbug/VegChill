from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.test import test
import os
import sys

APP_NAME = 'VegChill'
APP_AUTHOR = 'Anciety'

INSTALL_SCRIPT = r'''import os

config_path = {}
def __lldb_init_module(debugger, internal_dict):
    import vegchill
    vegchill.lldb_init_module(debugger, internal_dict, config_path)

if __name__ == '__main__':
    # gdb
    {}
    import vegchill
    vegchill.gdb_init_module(config_path)
'''

TEST_SCRIPT = r'''import unittest

def __lldb_init_module(debugger, internal_dict):
    unittest.main('tests', argv=['test_vegchill'])

if __name__ == '__main__':
    # gdb
    import sys
    sys.path.append('.')
    import vegchill
    import tests
    unittest.main('tests')
'''

def post_install_init(app_path, rewrite_config=True, develop=False):
    from six.moves import configparser as ConfigParser
    '''
    if sys.version_info >= (3, 0):
        import configparser as ConfigParser
    else:
        import ConfigParser
    '''
    app_config_path = os.path.join(app_path, 'config')
    app_install_script_path = os.path.join(app_path, 'load_vegchill.py')
    if rewrite_config or not os.path.exists(app_config_path):
        config = ConfigParser.ConfigParser()
        config.add_section('plugin')
        config.add_section('option')
        if develop:
            config.set('option', 'verbose', 'true')
        else:
            config.set('option', 'verbose', 'false')
        with open(app_config_path, 'w') as f:
            config.write(f)
    
    # write load script
    with open(app_install_script_path, 'w') as f:
        if develop:
            f.write(INSTALL_SCRIPT.format("config_path='develop_app/config'", r'''import sys
    sys.path.append('.')
'''))
        else:
            f.write(INSTALL_SCRIPT.format('', ''))
    if develop:
        app_test_script_path = os.path.join(app_path, 'test_vegchill.py')
        with open(app_test_script_path, 'w') as f:
            f.write(TEST_SCRIPT)


class PostDevelopCommand(develop):
    def run(self):
        develop_app_dir = 'develop_app'
        if not os.path.exists(develop_app_dir):
            os.mkdir(develop_app_dir)
        develop.run(self)
        post_install_init(develop_app_dir, develop=True)


class PostInstallCommand(install):
    def run(self):
        import appdirs
        app_path = user_data_dir(APP_NAME, APP_AUTHOR)
        if not os.path.exists(app_path):
            os.mkdir(app_path)
        install.run(self)
        post_install_init(app_path)


class TestCommand(test):
    def run_tests(self):
        # we need gdb or lldb to run tests, instead of running those directly.
        # thus we write our own
        import subprocess
        from subprocess import Popen
        # check for gdb and lldb installation
        gdb = False
        lldb = False
        try:
            if Popen('gdb -v'.split()).wait() == 0:
                gdb = True
        except:
            pass

        try:
            if Popen('lldb -v'.split()).wait() == 0:
                lldb = True
        except:
            pass

        if not gdb and not lldb:
            raise OSError('No gdb and lldb found')

        # gdb tests
        if gdb:
            print('Running gdb tests')
            with open(os.devnull, 'w') as fnull:
                p = Popen('gdb', stdin=subprocess.PIPE, stdout=fnull)
                p.stdin.write(b'source develop_app/test_vegchill.py\n')
                p.stdin.flush()
                # gdb can exit after unittest.main
                p.wait()
        if lldb:
            print('Running lldb tests')
            with open(os.devnull, 'w') as fnull:
                p = Popen('lldb', stdin=subprocess.PIPE, stdout=fnull)
                p.stdin.write(b'command script import develop_app/test_vegchill.py\n')
                p.stdin.flush()
                p.stdin.write(b'exit\n')
                p.stdin.flush()
                p.wait()
        

setup(
    name=APP_NAME,
    version='0.1.0',
    packages=find_packages('src'),
    install_requires=[
        'appdirs >= 1.4.3',
        'six >= 1.11.0',
    ],
    setup_requires=[
        'six >= 1.11.0',
    ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
        'test': TestCommand,
    },
    author=APP_AUTHOR,
    author_email='ding641880047@126.com',
    description='Veg Chickens lldb enhencement plugin',
    keywords='lldb plugin',
)
