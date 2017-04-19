import test_context

import unittest

from contextlib import redirect_stderr
import io

from qjira.log import Log

class LogTest(unittest.TestCase):

    def setUp(self):
        self.stdErr = io.StringIO()
        Log.debugLevel = 0

    def tearDown(self):
        Log.debugLevel = 0
        
    def test_error(self):
        with redirect_stderr(self.stdErr):
            Log.error('hello')
        self.assertEquals('[ERROR] hello\n', self.stdErr.getvalue())

    def test_info(self):
        Log.debugLevel = 1
        with redirect_stderr(self.stdErr):
            Log.info('hello')
        self.assertEquals('[INFO] hello\n', self.stdErr.getvalue())

    def test_debug(self):
        Log.debugLevel = 2
        with redirect_stderr(self.stdErr):
            Log.debug('hello')
        self.assertEquals('[DEBUG] hello\n', self.stdErr.getvalue())

    def test_verbose(self):
        Log.debugLevel = 3
        with redirect_stderr(self.stdErr):
            Log.verbose('hello')
        self.assertEquals('[VERBOSE] hello\n', self.stdErr.getvalue())

