import test_context

import unittest
import datetime

from qjira.dataprocessor import DataProcessor

import test_data

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        pass

    def test_process_story_cycle_times(self):
        dp = DataProcessor(test_data.singleSprintStory())
        rows = dp.rows()
        self.assertEqual(len(rows), 1)
        self.assertDictContainsSubset({
            'project_key': 'Test',
            'issuetype_name': 'Story',
            'issue_key': 123,
            'story_points': 3.0,
            'status_InProgress': datetime.date(2017,1,30),
            'status_Done': datetime.date(2017,1,31)
        }, rows[0])

    def test_process_story_cycle_times_negativedays_fix(self):
        dp = DataProcessor(test_data.negativeHistoryStory())
        rows = dp.rows()
        self.assertEqual(len(rows), 1)
        self.assertDictContainsSubset({
            'status_InProgress': datetime.date(2017,1,30),
            'status_Done': datetime.date(2017,1,31)
        }, rows[0])
    
    def test_process_story_sprints(self):
        dp = DataProcessor(test_data.singleSprintStory(), pivot='sprint')
        rows = dp.rows()
        self.assertEqual(len(rows), 1)
        self.assertDictContainsSubset({
            'project_key':'Test',
            'issuetype_name': 'Story',
            'issue_key':123,
            'story_points':3.0,
            'sprint_name':'Chambers Sprint 9',
            'sprint_startDate':datetime.date(2016,4,25),
            'sprint_endDate':datetime.date(2016,5,9)
        }, rows[0])

    def test_process_story_sprints_NONE(self):
        dp = DataProcessor(test_data.noSprintStory(), pivot='sprint')
        self.assertEqual(len(dp.rows()), 0)

    def test_process_story_sprints_NOPTS(self):
        dp = DataProcessor(test_data.zeroPointStory(), pivot='sprint')
        rows = dp.rows()
        self.assertEqual(len(rows), 1)
        with self.assertRaises(KeyError):
            rows[0]['story_points']
    
    def test_process_story_sprints_MULTI_SPRINT(self):
        dp = DataProcessor(test_data.multiSprintStory(), pivot='sprint')
        rows = dp.rows()
        self.assertEqual(len(rows), 2)

        start_id = 82
        for idx, row in enumerate(rows):
            self.assertDictContainsSubset({
                'sprint_id': str(start_id + idx)
            }, row)
