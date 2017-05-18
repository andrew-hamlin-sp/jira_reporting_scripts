import test_context

import unittest
import datetime

from qjira.cycletime import CycleTime

import test_data

class TestCycleTime(unittest.TestCase):

    def setUp(self):
        self.ct = CycleTime()

    def test_header(self):
        self.assertListEqual(['project_key','fixVersions_0_name','issuetype_name','issue_key','story_points','status_InProgress','status_End'], self.ct.header)

    def test_query(self):
        self.assertEquals('((issuetype = Story AND status in (Done, Accepted)) OR (issuetype = Bug AND status = Closed))', self.ct.query)

    @unittest.skip('Not implemented')
    def test_process(self):
        self.assertFalse(True)

