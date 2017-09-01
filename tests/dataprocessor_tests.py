from . import test_context

import unittest
import datetime

import io

from qjira.dataprocessor import DataProcessor

from . import test_data

class TestDataProcessor(unittest.TestCase):

    def test_process_story_cycle_times(self):
        dp = DataProcessor()
        rows = dp.transform(test_data.singleSprintStory())
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
        dp = DataProcessor()
        rows = dp.transform(test_data.negativeHistoryStory())
        self.assertEqual(len(rows), 1)
        self.assertDictContainsSubset({
            'status_InProgress': datetime.date(2017,1,30),
            'status_Done': datetime.date(2017,1,31)
        }, rows[0])
    
    def test_process_story_sprints(self):
        dp = DataProcessor(pivot='sprint')
        rows = dp.transform(test_data.multiSprintStory())
        self.assertEqual(len(rows), 2)
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
        dp = DataProcessor(pivot='sprint')
        rows = dp.transform(test_data.noSprintStory())
        self.assertEqual(len(rows), 0)

    def test_process_story_sprints_NOPTS(self):
        dp = DataProcessor(pivot='sprint')
        rows = dp.transform(test_data.zeroPointStory())
        self.assertEqual(len(rows), 1)
        with self.assertRaises(KeyError):
            rows[0]['story_points']

    def test_process_story_sprints_MULTI_SPRINT(self):
        dp = DataProcessor(pivot='sprint')
        rows = dp.transform(test_data.multiSprintStory())
        self.assertEqual(len(rows), 2)

        start_id = 82
        for idx, row in enumerate(rows):
            self.assertDictContainsSubset({
                'sprint_id': str(start_id + idx)
            }, row)

    def test_nested_data_flattens(self):
        dp = DataProcessor()
        rows = dp.transform(test_data.nested_data())
        self.assertEqual(len(rows), 1)
        #print({'k %s = v %s' % (k, type(v)) for k,v in rows[0].items() if type(v) == dict})
        row = rows[0]
        [self.assertFalse(type(v)==list, msg='flattened data contains list') for v in row.values()]
        [self.assertFalse(type(v)==dict, msg='flattened data contains dict') for v in row.values()]

        
