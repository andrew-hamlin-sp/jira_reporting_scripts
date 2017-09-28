from . import test_context

import unittest

from qjira.techdebt import TechDebtCommand

from . import test_data
from . import test_util

class TestTechDebt(test_util.MockJira, unittest.TestCase):

    def setUp(self):
        self.setup_mock_jira()
        self.command_under_test = TechDebtCommand(project=['TEST'],
                                                  base_url='localhost:3000')

    def tearDown(self):
        self.teardown_mock_jira()

    def test_header(self):
        self.assertIsInstance(self.command_under_test.header, list)

    def test_query(self):
        self.assertEqual(
            'issuetype in (Story, Bug) AND status in (Accepted, Closed, Done)',
            self.command_under_test .query)

    def test_process(self):
        self.json_response = {
            'total': 2,
            'issues': [test_data.singleSprintStory(), test_data.simpleBug()]
        }
        data = list(self.command_under_test.execute())
        self.assertEqual(len(data), 3)

        # project Test, type Story, points 3
        # project Test Two, type Bug, points 3
        self.assertDictEqual({'project_name':'Test',
                              'bug_points': '0',
                              'story_points': '3',
                              'tech_debt': '0%'},
                             data[0])
        self.assertDictEqual({'project_name':'Test Two',
                              'bug_points': '3',
                              'story_points': '0',
                              'tech_debt': '100%'},
                             data[1])
        self.assertDictEqual({'project_name':'Grand Total',
                              'bug_points': '3',
                              'story_points': '3',
                              'tech_debt': '50%'},
                             data[2])

    def test_process_no_points(self):
        bug = test_data.simpleBug()
        bug['fields']['customfield_10109'] = None
        self.json_response = {
            'total': 1,
            'issues': [bug]
        }
        data = list(self.command_under_test.execute())
        self.assertEqual(len(data), 2)

        # project Test Two, type Bug, points 0
        self.assertDictEqual({'project_name':'Test Two',
                              'bug_points': '0',
                              'story_points': '0',
                              'tech_debt': '0%'},
                             data[0])
        self.assertDictEqual({'project_name':'Grand Total',
                              'bug_points': '0',
                              'story_points': '0',
                              'tech_debt': '0%'},
                             data[1])
