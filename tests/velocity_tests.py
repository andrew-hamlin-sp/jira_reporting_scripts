import test_context

import unittest
import datetime
from dateutil.tz import tzoffset

from qjira.util import sprint_info
from qjira.velocity import Velocity

import test_data

class TestVelocity(unittest.TestCase):

    def test_sprint_info(self):
        self.assertEqual({'name':'Chambers Sprint 9',
                          'id':'82',
                          'rapidViewId':'52',
                          'state':'CLOSED',
                          'goal':'<null>',
                          'startDate':datetime.datetime(2016,4,25,10,44,22,273000, tzinfo=tzoffset(None,-18000)),
                          'endDate':datetime.datetime(2016,5,9,10,44,tzinfo=tzoffset(None,-18000)),
                          'completeDate':datetime.datetime(2016,5,9,10,48,4,212000, tzinfo=tzoffset(None,-18000)),
                          'sequence':'82'},
                         sprint_info(test_data.SPRINT1))

    def setUp(self):
        self.vel = Velocity(project=['Test'])
        self.jql = ''

    def update(self, jql):
        self.jql = jql
        
    def test_header(self):
        self.assertEquals('project,issue,points,carried,sprint,startDate,endDate', self.vel.header)

    def test_query(self):
        self.vel.query(lambda a: self.update(a))
        self.assertEquals('project in (Test) AND issuetype in (Story, Bug)', self.jql)
    
    def test_process_story_sprints(self):
        r = next(self.vel.process([test_data.STORY]))
        self.assertTupleEqual(('Test',123, 3.0, 0, 'Chambers Sprint 9', datetime.date(2016,4,25), datetime.date(2016,5,9)), r)

    def test_process_story_sprints_NONE(self):
        with self.assertRaises(StopIteration):
            next(self.vel.process([test_data.STORY_NO_SPRINT]))

    def test_process_story_sprints_NOPTS(self):
        r = next(self.vel.process([test_data.STORY_NO_POINTS]))
        self.assertTupleEqual(('Test',123, 0.0, 0, 'Chambers Sprint 10', datetime.date(2016,4,25), datetime.date(2016,5,9)), r)

    def test_process_story_sprints_NODATES(self):
        r = next(self.vel.process([test_data.STORY_NO_DATES]))
        self.assertTupleEqual(('Test',123, 5.0, 0, 'Sprint No Dates','',''), r)
    
    def test_process_story_sprints_BUG(self):
        r = next(self.vel.process([test_data.BUG]))
        self.assertTupleEqual(('IIQCB', 'IIQCB-668', 1.0, 0, '7.2 Cycle 1 - 1', datetime.date(2017, 1, 3), datetime.date(2017, 1, 13)), r)
