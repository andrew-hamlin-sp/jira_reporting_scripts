'''An ultra stupid logger'''
import sys
from six import print_

class Log:
    '''Simple logger'''

    # globals
    debugLevel = 0
    
    @staticmethod
    def eprint (msg, **kwargs):
        '''print args to stderr'''
        print_(msg, file=sys.stderr, **kwargs)

    @staticmethod
    def error (*msg):
        '''Log as an error'''
        msg = ' '.join(list(msg))
        Log.eprint('[ERROR] {}'.format(msg))

    @staticmethod
    def isErrorEnabled():
        return True
        
    @staticmethod
    def info (*msg):
        '''Log message when debug >= 0'''
        if Log.isInfoEnabled():
            msg = ' '.join(list(msg))
            Log.eprint('[INFO] {}'.format(msg))

    @staticmethod
    def isInfoEnabled ():
        if Log.debugLevel < 0:
            return False
        return True
        
    @staticmethod
    def debug (*msg):
        '''Log message when debug >= 1'''
        if Log.isDebugEnabled():
            msg = ' '.join(list(msg))
            Log.eprint('[DEBUG] {}'.format(msg))

    @staticmethod
    def isDebugEnabled ():
        if Log.debugLevel < 1:
            return False
        return True
        
    @staticmethod
    def verbose (*msg):
        '''Log message when debug >= 2'''
        if Log.isVerboseEnabled():
            msg = ' '.join(list(msg))
            Log.eprint('[VERBOSE] {}'.format(msg))

    @staticmethod
    def isVerboseEnabled ():
        if Log.debugLevel < 2:
            return False
        return True
