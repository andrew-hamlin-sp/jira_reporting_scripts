from . import test_context

import unittest
import datetime

from qjira.summary import Summary
from qjira.jira import Jira
#from qjira.container import Container

from . import test_data


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
        self.assertDictContainsSubset({'summary': 'CHAMBERS SPRINT 10  [2016-05-10 to 2016-05-19]'}, data[0])
        # summary command adds row for each story completed or in-progress for that sprint
        self.assertDictContainsSubset({'sprint_0_name': 'Chambers Sprint 10'}, data[1])
        # make sure resolve epic link is called properly
        self.assertDictContainsSubset({'epic_link': '=HYPERLINK("https://localhost/browse/test-1234","epic name")'}, data[1])

    def test_doc_links_marked_new(self):
        """Test that design doc and test plan links are annotated with *NEW* text"""

        data = self.processor.process([test_data.singleSprintStory()])
        self.assertEqual(len(data), 2) # summary adds a sprint header
        
        # original data will not be marked newline
        self.assertNotRegexpMatches(data[1].get('design_doc_link'), '\[New\]')
        self.assertNotRegexpMatches(data[1].get('testplan_doc_link'), '\[New\]')

        # modify the dates to mark these as News
        update_json = test_data.singleSprintStory()
        days_ago = datetime.datetime.utcnow()+datetime.timedelta(days=-14)
        for history in update_json['changelog']['histories']:
            history['created'] = days_ago.strftime('%Y-%m-%dT%H:%M:%S.000-0500')

        print(update_json['changelog']['histories'])
        data = self.processor.process([update_json])
        self.assertRegexpMatches(data[1].get('design_doc_link'), '\[New\]')
        self.assertRegexpMatches(data[1].get('testplan_doc_link'), '\[New\]')
