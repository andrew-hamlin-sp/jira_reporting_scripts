import test_context

import unittest

from contextlib import redirect_stderr
import io

from qjira.log import Log

class LogTest(unittest.TestCase):

    def setUp(self):
        self.std_err = io.StringIO()
        Log.debugLevel = 0

    def tearDown(self):
        Log.debugLevel = 0
        
    def test_error(self):
        with redirect_stderr(self.std_err):
            Log.error('hello')
        self.assertEquals('[ERROR] hello\n', self.std_err.getvalue())

    def test_info(self):
        Log.debugLevel = 1
        with redirect_stderr(self.std_err):
            Log.info('hello')
        self.assertEquals('[INFO] hello\n', self.std_err.getvalue())

    def test_debug(self):
        Log.debugLevel = 2
        with redirect_stderr(self.std_err):
            Log.debug('hello')
        self.assertEquals('[DEBUG] hello\n', self.std_err.getvalue())

    def test_verbose(self):
        Log.debugLevel = 3
        with redirect_stderr(self.std_err):
            Log.verbose('hello')
        self.assertEquals('[VERBOSE] hello\n', self.std_err.getvalue())

