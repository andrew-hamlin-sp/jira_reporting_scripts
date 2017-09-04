from . import test_context

import sys
import io
import unittest
import keyring
import keyring.backend

from requests.exceptions import HTTPError
from requests import Response

try:
    from contextlib import redirect_stdout
except ImportError:
    from contextlib2 import redirect_stdout

PY3 = sys.version_info[0] > 2

import qjira.__main__ as prog
from qjira.__main__ import UnicodeWriter

class FakeService:

    Raises401 = False
    
    def __init__(*args, **kwargs):
        pass

    def get_project_issues(self, *args, **kwargs):
        if self.Raises401:
            response = Response()
            response.status_code = 401
            raise HTTPError(response=response)
        return []

def _test_create_service(*args, **kwargs):
    return FakeService()

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
    

class TestMainCLI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        keyring.set_keyring(TestableKeyring())
        
    def setUp(self):
        keyring.get_keyring().entries['qjira-sp_userb'] = 'xyzzy'
        prog._create_service = _test_create_service
        self.std_out = io.StringIO() if PY3 else io.BytesIO()

    def tearDown(self):
        FakeService.Raises401 = False

    def test_stores_credentials(self):
        with redirect_stdout(self.std_out):
            prog.main(['s','-p','IIQCB','-w','blah','-u','usera'])
            
        self.assertEquals('blah', keyring.get_keyring().entries['qjira-sp_usera'])
        
    def test_not_authorized_clears_credentials(self):
        self.assertEquals('xyzzy', keyring.get_keyring().entries['qjira-sp_userb'])
        FakeService.Raises401 = True

        with redirect_stdout(self.std_out):
            with self.assertRaises(HTTPError):
                prog.main(['s','-p','IIQCB','-w','xyzzy','-u','userb'])
            
        with self.assertRaises(KeyError):
            keyring.get_keyring().entries['qjira-sp_userb']

    def test_unicode_writer_encodes_utf8(self):
        with redirect_stdout(self.std_out):
            writer = UnicodeWriter(sys.stdout, [u'summary'], encoding='utf-8')
            writer.writeheader()
            writer.writerow({u'summary': u'Performance optimization on \u201cMy access review\u201d widget on the home screen'})
        self.assertTrue(True)
        
    def test_unicode_writer_encodes_ascii(self):
        with redirect_stdout(self.std_out):
            writer = UnicodeWriter(sys.stdout, [u'summary'], encoding='ascii')
            writer.writeheader()
            writer.writerow({u'summary': u'Performance optimization on \u201cMy access review\u201d widget on the home screen'})
        self.assertTrue(True)
