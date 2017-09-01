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
        self.assertDictContainsSubset({'summary': 'CHAMBERS SPRINT 10  [05/10/2016 to 05/19/2016]'}, data[0])
        # summary command adds row for each story completed or in-progress for that sprint
        self.assertDictContainsSubset({'sprint_0_name': 'Chambers Sprint 10'}, data[1])
        # make sure resolve epic link is called properly
        self.assertDictContainsSubset({'epic_link': '=HYPERLINK("https://localhost/browse/test-1234","epic name")'}, data[1])

    def test_doc_links_marked_new(self):
        """Test that design doc and test plan links are annotated with *NEW* text"""

        # linked within past 14 day, mark with new
        row0 = {
            'link_url': 'https://localhost/my/doclink/DOC-1234',
            'link_changed': datetime.date.today()+datetime.timedelta(days=-14)
        }

        # linked earlier than past 14 days, not marked
        row1 = {
            'link_url': 'https://localhost/my/doclink/DOC-5678',
            'link_changed': datetime.date.today()+datetime.timedelta(days=-15)
        }

        from qjira.summary import doc_link_marked_new, hyperlink

        self.assertEquals(hyperlink(row0['link_url'], '[New] DOC-1234'), doc_link_marked_new(row0, 'link_url', 'link_changed'))
        self.assertEquals(hyperlink(row1['link_url'], 'DOC-5678'), doc_link_marked_new(row1, 'link_url', 'link_changed'))
