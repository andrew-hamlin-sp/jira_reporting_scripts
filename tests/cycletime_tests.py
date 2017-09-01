from . import test_context

import unittest
import datetime

from qjira.cycletime import CycleTime

from . import test_data

class TestCycleTime(unittest.TestCase):

    def setUp(self):
        self.processor = CycleTime()

    def test_header(self):
        self.assertIsInstance(self.processor.header, list)

    def test_query(self):
        self.assertEquals('issuetype = Story AND status in (Done, Accepted)', self.processor.query)

    def test_process(self):
        data = self.processor.process([test_data.multiSprintStory()])
        self.assertEqual(len(data), 1)
        # cycletime command will record the in-progress to done dates 
        self.assertDictContainsSubset(
            {'status_InProgress': '2017-01-30', 'status_Done':  '2017-01-31'}, data[0])
        # cycletime command will produce an Excel NETWORKDAYS formula
        self.assertDictContainsSubset({'count_days': '=NETWORKDAYS("2017-01-30","2017-01-31")'}, data[0])

    def test_process_done_wo_progress(self):
        data = self.processor.process([test_data.doneWithNoProgress()])
        self.assertEqual(len(data), 1)
        # cycletime command will record the in-progress to done dates 
        self.assertDictContainsSubset(
            {'status_InProgress': '2017-01-31', 'status_Done': '2017-01-31'}, data[0])
        # cycletime command will produce an Excel NETWORKDAYS formula
        self.assertDictContainsSubset({'count_days': '=NETWORKDAYS("2017-01-31","2017-01-31")'}, data[0])

    def test_process_accepted(self):
        data = self.processor.process([test_data.acceptedStory()])
        self.assertEqual(len(data), 1)
        # cycletime command will record the in-progress to done dates 
        self.assertDictContainsSubset(
            {'status_InProgress': '2017-01-30', 'status_Done': '2017-01-31'}, data[0])
