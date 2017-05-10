import test_context

import unittest
import datetime

from qjira.data import DataProcessor

import test_data

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        pass

    def test_process_story_cycle_times(self):
        dp = DataProcessor(test_data.STORY)
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

    def test_process_story_cycle_times_BUG(self):
        dp = DataProcessor(test_data.BUG)
        rows = dp.rows()
        self.assertEqual(len(rows), 1)
        self.assertDictContainsSubset({
            'project_key': 'IIQCB',
            'issuetype_name': 'Bug',
            'issue_key': 'IIQCB-668',
            'story_points': 1.0,
            'status_InProgress': datetime.date(2016, 12, 13),
            'status_Closed':datetime.date(2017, 1, 11)
        }, rows[0])

    def test_process_story_cycle_times_negativedays_fix(self):
        dp = DataProcessor(test_data.STORY_NEGATIVE_HISTORY)
        rows = dp.rows()
        self.assertEqual(len(rows), 1)
        self.assertDictContainsSubset({
            'status_InProgress': datetime.date(2017,1,30),
            'status_Done': datetime.date(2017,1,31)
        }, rows[0])
    
    def test_process_story_sprints(self):
        dp = DataProcessor(test_data.STORY, pivot='sprint')
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
        dp = DataProcessor(test_data.STORY_NO_SPRINT, pivot='sprint')
        self.assertEqual(len(dp.rows()), 0)

    def test_process_story_sprints_NOPTS(self):
        dp = DataProcessor(test_data.STORY_NO_POINTS, pivot='sprint')
        rows = dp.rows()
        self.assertEqual(len(rows), 1)
        with self.assertRaises(KeyError):
            rows[0]['story_points']
    
    def test_process_story_sprints_BUG(self):
        dp = DataProcessor(test_data.BUG, pivot='sprint')
        rows = dp.rows()
        self.assertEqual(len(rows), 1)
        self.assertDictContainsSubset({
            'project_key':'IIQCB',
            'issuetype_name': 'Bug',
            'issue_key': 'IIQCB-668',
            'story_points': 1.0,
            'sprint_name': '7.2 Cycle 1 - 1',
            'sprint_startDate': datetime.date(2017, 1, 3),
            'sprint_endDate': datetime.date(2017, 1, 13)
        }, rows[0])

    def test_process_story_sprints_MULTI_SPRINT(self):
        dp = DataProcessor(test_data.STORY_MULTI_SPRINT, pivot='sprint')
        rows = dp.rows()
        self.assertEqual(len(rows), 2)

        start_id = 82
        for idx, row in enumerate(rows):
            self.assertDictContainsSubset({
                'sprint_id': str(start_id + idx)
            }, row)
