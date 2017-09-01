from . import test_context

import unittest

from qjira.jira import Jira

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

class TestJira(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.jira_under_test = Jira("localhost:3000")
        self.jira_under_test._get_json = self._get_json_assert

        self.expectedUrl = None

    def _get_json_assert(self, url):
        parts = urlparse(url)
        expectedParts = urlparse(self.expectedUrl)
        self.assertEqual(expectedParts.path, parts.path)
        self.assertEqual(parse_qs(expectedParts.query), parse_qs(parts.query))
        return {'total': 0, 'issues': []}
        
    def test_get_project_issues(self):
        """test that all expected fields are urlencoded properly""" 

        self.expectedUrl = 'https://localhost:3000/rest/api/2/search?fields=-%2Anavigable%2Cproject%2Cissuetype%2Cstatus%2Csummary%2Cassignee%2CfixVersions%2Ccustomfield_10109%2Ccustomfield_10016%2Ccustomfield_11101%2Ccustomfield_14300%2Ccustomfield_10017&jql=issuetype+%3D+Story&startAt=0&maxResults=50&expand=changelog'
        self.jira_under_test.get_project_issues('issuetype = Story')

    def test_get_browse_url(self):
        url = self.jira_under_test.get_browse_url('IIQETN-1')

        self.assertEqual('https://localhost:3000/browse/IIQETN-1', url)

    def test_get_issue(self):
        """Test that getting a single issue urlencodes properly"""

        self.expectedUrl = 'https://localhost:3000/rest/api/2/issue/IIQETN-1'
        self.jira_under_test.get_issue('IIQETN-1')
