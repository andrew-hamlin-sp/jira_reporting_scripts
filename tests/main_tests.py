import test_context

import unittest

import keyring
import keyring.backend

from contextlib import redirect_stdout
import io

from requests.exceptions import HTTPError
from requests import Response

import qjira.__main__ as prog

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

def _test_create_service(*args):
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
        self.std_out = io.StringIO()
        prog._create_service = _test_create_service

    def tearDown(self):
        FakeService.Raises401 = False
        
    def test_with_empty_args(self):
        with self.assertRaises(SystemExit):
            with redirect_stdout(self.std_out):
                prog.main([])
                
        self.assertRegex(self.std_out.getvalue(), 'usage:')
        
    def test_stores_credentials(self):
        with redirect_stdout(self.std_out):
            prog.main(['s','-p','IIQCB','-w','xyzzy','-u','usera'])

        self.assertEquals('xyzzy', keyring.get_keyring().entries['qjira-sp_usera'])
        
    def test_not_authorized_clears_credentials(self):
        self.assertEquals('xyzzy', keyring.get_keyring().entries['qjira-sp_userb'])
        FakeService.Raises401 = True
        
        with self.assertRaises(HTTPError):
            prog.main(['s','-p','IIQCB','-w','xyzzy','-u','userb'])
            
        with self.assertRaises(KeyError):
            keyring.get_keyring().entries['qjira-sp_userb']

