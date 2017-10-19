from . import test_context

import sys
import io
import unittest
import keyring
import keyring.backend
import re
import os
import tempfile

from requests.exceptions import HTTPError
from requests import Response

try:
    from contextlib import redirect_stdout, redirect_stderr
except ImportError:
    from contextlib2 import redirect_stdout, redirect_stderr

import qjira.__main__ as prog

from . import test_util
from . import test_data

PY3 = sys.version_info > (3,)

class TestableKeyring(keyring.backend.KeyringBackend):

    priority = 1

    entries = dict()

    def _key(self, servicename, username):
        key = "{0}_{1}".format(servicename, username)
        return key
    
    def set_password(self, servicename, username, password):
        key = self._key(servicename, username)       
        self.entries[key] = password

    def get_password(self, servicename, username):
        key = self._key(servicename, username)
        return self.entries[key]

    def delete_password(self, servicename, username):
        key = self._key(servicename, username)
        del self.entries[key]
    

class TestMainCLI(test_util.SPTestCase, test_util.MockJira, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        keyring.set_keyring(TestableKeyring())
        
    def setUp(self):
        keyring.get_keyring().entries['qjira-sp_userb'] = 'xyzzy'
        self.std_out = io.StringIO() if PY3 else io.BytesIO()
        self.std_err = io.StringIO() if PY3 else io.BytesIO()

        self.setup_mock_jira()

    def tearDown(self):
        self.teardown_mock_jira()

    def test_stores_credentials(self):
        with redirect_stdout(self.std_out):
            with redirect_stderr(self.std_err):
                prog.main(['cycletime','-w','blah','-u','usera', 'IIQCB'])
            
        self.assertEqual('blah', keyring.get_keyring().entries['qjira-sp_usera'])
        
    def test_not_authorized_clears_credentials(self):
        self.assertEqual('xyzzy', keyring.get_keyring().entries['qjira-sp_userb'])
        self.raise401 = True
        
        with redirect_stdout(self.std_out):
            with redirect_stderr(self.std_err):
                prog.main(['cycletime','-w','xyzzy','-u','userb', 'IIQCB'])

        error_msg = self.std_err.getvalue()
        self.assertRegex_(error_msg, r'[ERROR].*Unauthorized')
                
        with self.assertRaises(KeyError):
            keyring.get_keyring().entries['qjira-sp_userb']

    def test_progress_shown(self):
        re_1of1 = re.compile('Retrieved 1 issue')
        self.json_response = {
            'total': 1,
            'issues': [test_data.singleSprintStory()]
        }
        with redirect_stdout(self.std_out):
            with redirect_stderr(self.std_err):
                prog.main(['cycletime', '-w', 'blah', 'TEST'])

        self.assertRegex_(self.std_err.getvalue(), re_1of1)

    def test_progress_hidden(self):
        re_1of1 = re.compile('Retrieved 1 issue')
        self.json_response = {
            'total': 1,
            'issues': [test_data.singleSprintStory()]
        }
        with redirect_stderr(self.std_err):
            with redirect_stdout(self.std_out):
                prog.main(['cycletime', '-w', 'blah', '--no-progress', 'TEST'])

        self.assertNotRegex_(self.std_err.getvalue(), re_1of1)

    def test_write_to_file(self):
        f, path = tempfile.mkstemp(suffix='csv')
        self.json_response = {
            'total': 1,
            'issues': [test_data.singleSprintStory()]
        }
        lines = None
        try:
            with redirect_stderr(self.std_err):
                with redirect_stdout(self.std_out):
                    prog.main(['cycletime', '-w', 'blah', '--no-progress', '-o', path, 'TEST'])
            with open(path, 'r') as o:
                lines = o.readlines()
        finally:
            os.unlink(path)
        self.assertEqual(2, len(lines))


    def test_command_options_require_project(self):

        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(self.std_err):
                prog.main(['cycletime', '-w', 'blah', '--no-progress'])
        exc = ctx.exception
        self.assertEqual(exc.code, 2)
        self.assertRegex_(self.std_err.getvalue(), r'cycletime: error: too few arguments')

    
    def test_command_jql_require_jql(self):
        with self.assertRaises(SystemExit) as ctx:
            with redirect_stderr(self.std_err):
                prog.main(['jql', '-w', 'blah', '--no-progress'])
        exc = ctx.exception
        self.assertEqual(exc.code, 2)
        self.assertRegex_(self.std_err.getvalue(), r'jql: error: too few arguments')
