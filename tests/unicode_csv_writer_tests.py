from . import test_context

import sys
import io
import unittest
import re
from collections import OrderedDict

try:
    from contextlib import redirect_stdout
except ImportError:
    from contextlib2 import redirect_stdout

import qjira.unicode_csv_writer as csv_writer

from qjira.command import BaseCommand
from . import test_data
from . import test_util

PY3 = sys.version_info > (3,)

class TestCommand(BaseCommand):

    @property
    def header(self):
        return OrderedDict([('summary', 'Summary')])

    @property
    def query(self):
        return ''

class TestCommandTestCase(test_util.SPTestCase, test_util.MockJira, unittest.TestCase):

    def setUp(self):
        '''Setup for unicode tests require special handling for python version.'''
        self.std_out = io.StringIO() if PY3 else io.BytesIO()

        self.setup_mock_jira()

        self.json_response = {
            'total': 1,
            'issues': [test_data.singleSprintStory()]
        }
        
        # delegate to non-abstract test case
        self._setup()

    def tearDown(self):
        self.teardown_mock_jira()

    def getColumns(self, val):
        lines = val.splitlines()
        cols = lines[0].split(',')
        return cols

class TestUnicodeWriter(TestCommandTestCase):

    def _setup(self):
        self.command = TestCommand(project=['TEST'], base_url='localhost:3000')
    
    def test_unicode_writer_encodes_ascii(self):
        '''Test that csv encoding converts unicode to ascii'''
        utf8_re = re.compile('\u201c.+\u201d', flags=re.UNICODE)
        with redirect_stdout(self.std_out):
            csv_writer.write(sys.stdout, self.command, 'ASCII')
        self.assertNotRegex_(self.std_out.getvalue(), utf8_re)

    def test_header_written_ok(self):
        with redirect_stdout(self.std_out):
            csv_writer.write(sys.stdout, self.command, 'ASCII')        
        cols = self.getColumns(self.std_out.getvalue())
        self.assertEqual(1, len(cols))

    @unittest.skipIf(sys.version_info < (3,),
                     'This version of csv module does not support utf8 encoding')
    def test_unicode_writer_encodes_utf8(self):
        '''Test that csv encoding supports utf-8 option.'''
        utf8_re = re.compile('\u201c.+\u201d', flags=re.UNICODE)
        with redirect_stdout(self.std_out):
            csv_writer.write(sys.stdout, self.command, 'UTF-8')
        self.assertRegex_(self.std_out.getvalue(), utf8_re)

class TestAllFields(TestCommandTestCase):

    def _setup(self):
        self.command = TestCommand(project=['TEST'], base_url='localhost:3000', all_fields=True)

    def test_header_written_ok(self):
        self.assertTrue(self.command.show_all_fields)
        with redirect_stdout(self.std_out):
            csv_writer.write(sys.stdout, self.command, 'ASCII')
        cols = self.getColumns(self.std_out.getvalue())
        self.assertTrue(1 < len(cols))
