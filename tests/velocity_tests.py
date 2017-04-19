import test_context

import unittest
import datetime

from qjira.util import sprint_info
from qjira.velocity import Velocity

import test_data

class TestVelocity(unittest.TestCase):

    def test_sprint_info(self):
        self.assertEqual({'name':'Chambers Sprint 9','id':'82','rapidViewId':'52','state':'CLOSED','goal':'<null>','startDate':'2016-04-25T10:44:22.273-05:00','endDate':'2016-05-09T10:44:00.000-05:00','completeDate':'2016-05-09T10:48:04.212-05:00','sequence':'82'}, sprint_info(test_data.SPRINT1))

    def setUp(self):
        self.vel = Velocity(project=['Test'])
        self.jql = ''

    def update(self, jql):
        self.jql = jql
        
    def test_header(self):
        self.assertEquals('issue,points,sprint,startDate,endDate', self.vel.header)

    def test_query(self):
        self.vel.query(lambda a: self.update(a))
        self.assertEquals('project in (Test) AND issuetype = Story', self.jql)
    
    def test_process_story_sprints(self):
        r = next(self.vel.process([test_data.STORY]))
        self.assertTupleEqual((123, 3.0, 'Chambers Sprint 9', datetime.date(2016,4,25), datetime.date(2016,5,9)), r)

    def test_process_story_sprints_NONE(self):
        r = next(self.vel.process([test_data.STORY_NO_SPRINT]))
        self.assertTupleEqual((123, 3.0, '','',''), r)

    def test_process_story_sprints_NOPTS(self):
        r = next(self.vel.process([test_data.STORY_NO_POINTS]))
        self.assertTupleEqual((123, 0.0, 'Chambers Sprint 10', datetime.date(2016,4,25), datetime.date(2016,5,9)), r)

