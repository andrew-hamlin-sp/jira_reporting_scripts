from . import test_context

import sys
import io
import unittest
import re

try:
    from contextlib import redirect_stdout
except ImportError:
    from contextlib2 import redirect_stdout

import qjira.unicode_csv_writer as csv_writer
import qjira.jira as j

from qjira.command import BaseCommand
from . import test_data
from . import test_util

PY3 = sys.version_info > (3,)

class TestCommand(BaseCommand):

    @property
    def header(self):
        return ['summary']

    @property
    def query(self):
        return ''
    

class TestUnicodeWriter(test_util.SPTestCase, test_util.MockJira, unittest.TestCase):

    def setUp(self):
        '''Setup for unicode tests require special handling for python version.'''
        self.std_out = io.StringIO() if PY3 else io.BytesIO()

        self.setup_mock_jira(j)
        self.command = TestCommand(project=['TEST'], base_url='localhost:3000')

        self.json_response = {
            'total': 1,
            'issues': [test_data.singleSprintStory()]
        }

    def tearDown(self):
        self.teardown_mock_jira(j)

    def test_unicode_writer_encodes_ascii(self):
        '''Test that csv encoding converts unicode to ascii'''
        utf8_re = re.compile('\u201c.+\u201d', flags=re.UNICODE)
        with redirect_stdout(self.std_out):
            csv_writer._write_encoded(sys.stdout, self.command, 'ASCII')
        self.assertNotRegex_(self.std_out.getvalue(), utf8_re)

    @unittest.skipIf(sys.version_info < (3,),
                     'This version of csv module does not support utf8 encoding')
    def test_unicode_writer_encodes_utf8(self):
        '''Test that csv encoding supports utf-8 option.'''
        utf8_re = re.compile('\u201c.+\u201d', flags=re.UNICODE)
        with redirect_stdout(self.std_out):
            csv_writer._write_encoded(sys.stdout, self.command, 'UTF-8')
        self.assertRegex_(self.std_out.getvalue(), utf8_re)
