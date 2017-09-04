from . import test_context

import unittest

from qjira.backlog import Backlog

from . import test_data

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

    def test_process_1(self):
        data = self.processor.process([test_data.singleSprintStory()])
        self.assertEqual(len(data), 1)
        
        self.assertDictContainsSubset({
            'customer': 3,
            'priority_name': 'High',
            'severity_value': 'Normal'
        }, data[0])
