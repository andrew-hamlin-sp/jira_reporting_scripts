'''An ultra stupid logger'''
import sys
from six import text_type, print_

class Log:
    '''Simple logger'''

    # globals
    debugLevel = 0
    
    @staticmethod
    def eprint (msg, *args, **kwargs):
        '''print args to stderr'''
        print_(text_type(msg).encode(), file=sys.stderr, **kwargs)

    @staticmethod
    def error (msg):
        '''Log as an error'''
        Log.eprint('[ERROR] {}'.format(msg))

    @staticmethod
    def isErrorEnabled():
        return True
        
    @staticmethod
    def info (msg):
        '''Log message when debug >= 0'''
        if Log.isInfoEnabled():
            Log.eprint('[INFO] {}'.format(msg))

    @staticmethod
    def isInfoEnabled ():
        if Log.debugLevel < 0:
            return False
        return True
        
    @staticmethod
    def debug (msg):
        '''Log message when debug >= 1'''
        if Log.isDebugEnabled():
            Log.eprint('[DEBUG] {}'.format(msg))

    @staticmethod
    def isDebugEnabled ():
        if Log.debugLevel < 1:
            return False
        return True
        
    @staticmethod
    def verbose (msg):
        '''Log message when debug >= 2'''
        if Log.isVerboseEnabled():
            Log.eprint('[VERBOSE] {}'.format(msg))

    @staticmethod
    def isVerboseEnabled ():
        if Log.debugLevel < 2:
            return False
        return True
