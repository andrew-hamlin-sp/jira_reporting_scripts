from . import test_context

import unittest
import datetime

import qjira.unicode_csv_writer as csv_writer_cls
import qjira.summary_html_writer as html_writer_cls

from qjira.summary import SummaryCommand

from . import test_data
from . import test_util

class TestSummaryAsCSV(test_util.SPTestCase, test_util.MockJira, unittest.TestCase):

    def setUp(self):
        self.setup_mock_jira()
        self.command_under_test = SummaryCommand(base_url='localhost:3000', project=['TEST'], use_csv_formatter=True)

    def tearDown(self):
        self.teardown_mock_jira()
        
    def test_header(self):
        self.assertIsInstance(self.command_under_test.header_keys, list)
        
    def test_query(self):
        self.assertEqual('issuetype = Story', self.command_under_test.query)

    def test_process(self):
        self.json_response = (x for x in [
            {
                'total': 1,
                'issues': [test_data.multiSprintStory()]
            },
            {
                'key': 10,
                'fields':{'customfield_10019':'epic name'}
            }
        ])
        data = list(self.command_under_test.execute())

        self.assertEqual(len(data), 2)
        # summary command groups by assigned sprint and inserts single SUMMARY row
        self.assertDictContainsSubset({'issue_link': 'CHAMBERS SPRINT 10  [2017-01-28 to 2017-02-07]'}, data[0])
        # summary command adds row for each story completed or in-progress for that sprint
        self.assertDictContainsSubset({'sprint_0_name': 'Chambers Sprint 10'}, data[1])
        # make sure resolve epic link is called properly
        self.assertDictContainsSubset({'epic_link': '=HYPERLINK("https://localhost:3000/browse/test-1234","epic name")'}, data[1])

    def test_doc_links_not_marked_new_without_new_opt(self):
        # modify the dates to mark these as News
        update_json = test_data.singleSprintStory()
        days_ago = datetime.datetime.utcnow()+datetime.timedelta(days=-14)
        for history in update_json['changelog']['histories']:
            history['created'] = days_ago.strftime('%Y-%m-%dT%H:%M:%S.000-0500')
        self.json_response = {
            'total': 1,
            'issues': [update_json]
        }
        data = list(self.command_under_test.execute())

        self.assertEqual(len(data), 2) # summary adds a sprint header
        
        self.assertNotRegex_(data[1].get('design_doc_link'), '\[New\]')
        self.assertNotRegex_(data[1].get('testplan_doc_link'), '\[New\]')

    def test_summary_writer(self):

        self.assertIs(self.command_under_test.writer, csv_writer_cls)
        self.assertIsNot(self.command_under_test.writer, html_writer_cls)

        
class TestSummaryNewOpt(test_util.SPTestCase, test_util.MockJira, unittest.TestCase):

    def setUp(self):
        self.setup_mock_jira()
        self.command_under_test = SummaryCommand(base_url='localhost:3000', project=['TEST'], mark_if_new=True)

    def tearDown(self):
        self.teardown_mock_jira()
        
    def test_doc_links_not_marked_new_when_old(self):
        """Test that design doc and test plan links are annotated with *NEW* text"""

        self.json_response = {
            'total': 1,
            'issues': [test_data.singleSprintStory()]
        }
        data = list(self.command_under_test.execute())

        self.assertEqual(len(data), 2) # summary adds a sprint header
        
        # original data will not be marked newline
        self.assertNotRegex_(data[1].get('design_doc_link'), '\[New\]')
        self.assertNotRegex_(data[1].get('testplan_doc_link'), '\[New\]')

    def test_doc_links_marked_new_when_new(self):
        # modify the dates to mark these as News
        update_json = test_data.singleSprintStory()
        days_ago = datetime.datetime.utcnow()+datetime.timedelta(days=-14)
        for history in update_json['changelog']['histories']:
            history['created'] = days_ago.strftime('%Y-%m-%dT%H:%M:%S.000-0500')
        self.json_response = {
            'total': 1,
            'issues': [update_json]
        }
        data = list(self.command_under_test.execute())

        self.assertEqual(len(data), 2) # summary adds a sprint header
        
        self.assertRegex_(data[1].get('design_doc_link'), '\[New\]')
        self.assertRegex_(data[1].get('testplan_doc_link'), '\[New\]')

class TestSummaryAsHTML(test_util.SPTestCase, test_util.MockJira, unittest.TestCase):

    def setUp(self):
        self.setup_mock_jira()
        self.command_under_test = SummaryCommand(base_url='localhost:3000', project=['TEST'])

    def tearDown(self):
        self.teardown_mock_jira()

    def test_summary_writer(self):
        self.assertIsNot(self.command_under_test.writer, csv_writer_cls)
        self.assertIs(self.command_under_test.writer, html_writer_cls)

    def test_process(self):
        self.json_response = (x for x in [
            {
                'total': 1,
                'issues': [test_data.multiSprintStory()]
            },
            {
                'key': 10,
                'fields':{'customfield_10019':'epic name'}
            }
        ])
        data = list(self.command_under_test.execute())

        self.assertEqual(len(data), 2)
        # summary command groups by assigned sprint and inserts single SUMMARY row
        self.assertDictContainsSubset({'issue_link': 'CHAMBERS SPRINT 10  [2017-01-28 to 2017-02-07]'}, data[0])
        # summary command adds row for each story completed or in-progress for that sprint
        self.assertDictContainsSubset({'sprint_0_name': 'Chambers Sprint 10'}, data[1])
        # make sure resolve epic link is called properly
        self.assertDictContainsSubset({'epic_link': '<a href="https://localhost:3000/browse/test-1234" target="_blank">epic name</a>'}, data[1])
