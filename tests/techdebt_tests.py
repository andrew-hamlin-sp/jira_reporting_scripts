from . import test_context

import unittest

from qjira.techdebt import TechDebt

from . import test_data

class TestTechDebt(unittest.TestCase):

    def setUp(self):
        self.processor = TechDebt()

    def test_header(self):
        self.assertIsInstance(self.processor.header, list)

    def test_query(self):
        self.assertEquals('issuetype in (Story, Bug) AND status in (Accepted, Closed, Done)', self.processor.query)

    def test_process(self):
        data = self.processor.process([test_data.singleSprintStory(), test_data.simpleBug()])
        self.assertEquals(len(data), 3)

        # project Test, type Story, points 3
        # project Test Two, type Bug, points 3
        self.assertDictEqual({'project_name':'Test', 'bug_points': '0', 'story_points': '3', 'tech_debt': '0%'}, data[0])
        self.assertDictEqual({'project_name':'Test Two', 'bug_points': '3', 'story_points': '0', 'tech_debt': '100%'}, data[1])
        self.assertDictEqual({'project_name':'Grand Total', 'bug_points': '3', 'story_points': '3', 'tech_debt': '50%'}, data[2])
