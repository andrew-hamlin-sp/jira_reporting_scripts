import getpass
import keyring

from .log import Log

KEYRING_NAME = 'qjira-sp'

def get_credentials(username, password):
    if not username:
        username = getpass.getuser()

    _needs_storage = True
    
    if not password:
        # retrieve password from system storage
        if keyring.get_keyring():
            password = keyring.get_password(KEYRING_NAME, username)
            if password:
                _needs_storage = False

    if not password:
        password = getpass.getpass('Enter password for {}: '.format(username))
        
    if _needs_storage and keyring.get_keyring():
        try:
            keyring.set_password(KEYRING_NAME, username, password)
        except keyring.errors.PasswordSetError as err:
            Log.error(err)
        
    return username, password

def clear_credentials(username):
    if username and keyring.get_keyring():
        try:
            keyring.delete_password(KEYRING_NAME, username)
        except keyring.errors.PasswordDeleteError as err:
            Log.error(err)
            
