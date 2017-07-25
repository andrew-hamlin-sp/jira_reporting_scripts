import test_context

import unittest

from qjira.summary import Summary
from qjira.jira import Jira
#from qjira.container import Container

import test_data

class TestSummary(unittest.TestCase):

    def setUp(self):
        service = Jira('localhost')
        service.get_issue = lambda k: {'fields':{'customfield_10019':'epic name'}}
        
        self.processor = Summary(service)

    def test_header(self):
        self.assertIsInstance(self.processor.header, list)

    def test_query(self):
        self.assertEquals('issuetype = Story', self.processor.query)

    def test_process(self):
        data = self.processor.process([test_data.multiSprintStory()])
        self.assertEquals(len(data), 2)
        # summary command groups by assigned sprint and inserts single SUMMARY row
        self.assertDictContainsSubset({'summary': 'CHAMBERS SPRINT 10  [05/10/2016 to 05/19/2016]'}, data[0])
        # summary command adds row for each story completed or in-progress for that sprint
        self.assertDictContainsSubset({'sprint_0_name': 'Chambers Sprint 10'}, data[1])
        # make sure resolve epic link is called properly
        self.assertDictContainsSubset({'epic_link': '=HYPERLINK("https://localhost/browse/test-1234","epic name")'}, data[1])
