import test_context

import unittest
import datetime

from qjira.cycletime import CycleTime

import test_data

class TestCycleTime(unittest.TestCase):

    def setUp(self):
        self.ct = CycleTime(project=['Test'])
        self.jql = ''

    def update(self, jql):
        self.jql = jql

    def test_header(self):
        self.assertEquals('issue,points,start,end', self.ct.header)

    def test_query(self):
        self.ct.query(lambda a: self.update(a))
        self.assertEquals('project in (Test) AND issuetype = Story AND status in (Done, Accepted)', self.jql)
        
    def test_process_story_cycle_times(self):
        r = next(self.ct.process([test_data.STORY]))
        self.assertTupleEqual((123,3.0,datetime.date(2017,1,30),datetime.date(2017,1,31)), r)

