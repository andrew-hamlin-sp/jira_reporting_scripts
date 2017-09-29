from . import test_context
import unittest

from qjira.jql import JQLCommand

from . import test_data
from . import test_util

class TestJQLCommand(test_util.MockJira, unittest.TestCase):

    _jql_param = 'project = IIQETN AND issuetype = Bug'
    
    def setUp(self):
        self.setup_mock_jira()
        self.command = JQLCommand(base_url='localhost:3000', jql=TestJQLCommand._jql_param)

    def tearDown(self):
        self.teardown_mock_jira()

    def test_query(self):
        self.assertEqual(TestJQLCommand._jql_param, self.command.query)

    def test_process(self):
        bug = test_data.simpleBug()
        self.json_response = {
            'total': 1,
            'issues': [bug]
        }
        data = list(self.command.execute())
        self.assertEqual(len(data), 1)


    def test_header(self):
        bug = test_data.simpleBug()
        self.json_response = {
            'total': 1,
            'issues': [bug]
        }
        row = next(self.command.execute())
        cols = self.command.expand_header(row.keys())
        self.assertListEqual(['project_key', 'issue_key','issuetype_name',
                              'summary', 'status_name', 'assignee_name', 'sprint_0_name',
                              'fixVersions_0_name'], cols)

class TestJQLCommandWithAdditionalFieldsColumns(test_util.MockJira, unittest.TestCase):

    def setUp(self):
        self.setup_mock_jira()
        self.command = JQLCommand(base_url='localhost:3000', jql=TestJQLCommand._jql_param, field=['customer'], column=['customer_0_value'])

    def tearDown(self):
        self.teardown_mock_jira()

    def test_add_fields(self):
        self.assertIn('customer', self.command.retrieve_fields(['foo', 'bar']))

    def test_add_columns(self):
        self.assertIn('customer_0_value', self.command.expand_header({}))
