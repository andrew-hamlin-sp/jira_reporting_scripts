import test_context

import unittest

from qjira.backlog import Backlog

import test_data

class TestBacklog(unittest.TestCase):

    def setUp(self):
        self.processor = Backlog()

    def test_header(self):
        self.assertIsInstance(self.processor.header, list)

    def test_query(self):
        self.assertEquals('issuetype = Bug AND resolution = Unresolved ORDER BY priority DESC', self.processor.query)

    def test_process_0(self):
        data = self.processor.process([])
        self.assertEqual(len(data), 0)

    
