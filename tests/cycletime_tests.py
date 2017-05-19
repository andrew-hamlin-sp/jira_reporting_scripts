import test_context

import unittest

from qjira.cycletime import CycleTime

import test_data

class TestCycleTime(unittest.TestCase):

    def setUp(self):
        self.processor = CycleTime(None)

    def test_header(self):
        self.assertIsInstance(self.processor.header, list)

    def test_query(self):
        self.assertEquals('((issuetype = Story AND status in (Done, Accepted)) OR (issuetype = Bug AND status = Closed))', self.processor.query)

    @unittest.skip('Not implemented')
    def test_process(self):
        self.assertFalse(True)

