from __future__ import print_function
import sys


class Log:
    '''Simple logger'''

    # globals
    global_DEBUG = 0
    
    def eprint (*args, **kwargs):
        '''print args to stderr'''
        print(*args, file=sys.stderr, **kwargs)
        
    eprint = eprint

    def error (*msg):
        '''Log as an error'''
        Log.eprint('[ERROR]', *msg)
        
    def info (*msg):
        '''Log message when debug >= 0'''
        if Log.global_DEBUG < 0:
            return
        Log.eprint('[INFO]', *msg)

    info = staticmethod(info)

    def debug (*msg):
        '''Log message when debug >= 1'''
        if Log.global_DEBUG < 1:
            return
        Log.eprint('[DEBUG]', *msg)

    debug = staticmethod(debug)
        
    def verbose (*msg):
        '''Log message when debug >= 2'''
        if Log.global_DEBUG < 2:
            return
        Log.eprint('[VERBOSE]', *msg)

    verbose = staticmethod(verbose)

