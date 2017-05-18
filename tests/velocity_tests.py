import test_context

import unittest
import datetime
from dateutil.tz import tzoffset

#from qjira.util import sprint_info
from qjira.velocity import Velocity

import test_data

class TestVelocity(unittest.TestCase):

    def setUp(self):
        self.vel = Velocity()

    def test_header(self):
        self.assertListEqual(self.vel.header, ['project_key','fixVersions_0_name','issuetype_name','issue_key','sprint_name','sprint_startDate','sprint_endDate','story_points','planned_points','carried_points','completed_points'])

    def test_query(self):
        self.assertEquals('issuetype in (Story, Bug)', self.vel.query)

    @unittest.skip('Not implemented')
    def test_process(self):
        pass
