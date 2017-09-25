from . import test_context

import unittest

from qjira.backlog import BacklogCommand
import qjira.jira as j

from . import test_data
from . import test_util

class TestBacklog(test_util.MockJira, unittest.TestCase):

    def setUp(self):
        self.setup_mock_jira(j)
        self.processor = BacklogCommand(project=['TEST'], base_url='localhost:3000')

    def tearDown(self):
        self.teardown_mock_jira(j)
        
    def test_header(self):
        self.assertIsInstance(self.processor.header, list)

    def test_query(self):
        self.assertEqual('issuetype = Bug AND resolution = Unresolved ORDER BY priority DESC', self.processor.query)

    def test_process_0(self):
        data = list(self.processor.execute())
        self.assertEqual(len(data), 0)

    def test_process_1(self):
        '''Backlog needs to pivot on the fixVersion'''
        self.json_response = {
            'total': 1,
            'issues': [test_data.singleSprintStory()]
        }
        data = list(self.processor.execute())
        self.assertEqual(len(data), 2)
        
        self.assertDictContainsSubset({
            'customer': 3,
            'priority_name': 'High',
            'severity_value': 'Normal'
        }, data[0])

        self.assertUrlPartsEqual('http://localhost:3000/rest/api/2/search?fields=-%2Anavigable%2Cproject%2Cissuetype%2Cstatus%2Csummary%2Cassignee%2CfixVersions%2Ccustomfield_10109%2Ccustomfield_10016%2Ccustomfield_10017%2Cpriority%2Ccreated%2Cupdated%2Ccustomfield_10112%2Ccustomfield_10400&jql=project+in+(TEST)+AND+issuetype+%3D+Bug+AND+resolution+%3D+Unresolved+ORDER+BY+priority+DESC&startAt=0&maxResults=50&expand=changelog', self.actual_url)
