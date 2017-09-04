from . import test_context

import unittest

from qjira.velocity import Velocity

from . import test_data

class TestVelocity(unittest.TestCase):

    def setUp(self):
        self.processor = Velocity()
        self.processor_includes_bugs = Velocity(include_bugs=True)

    def test_header(self):
        self.assertIsInstance(self.processor.header, list)
        
    def test_query(self):
        self.assertEquals('issuetype = Story', self.processor.query)
        self.assertEquals('issuetype in (Story, Bug)', self.processor_includes_bugs.query)

    def test_process_0(self):
        data = self.processor.process([])
        self.assertEqual(len(data), 0)
        
    def test_process(self):
        data = self.processor.process([test_data.multiSprintStory()])
        self.assertEqual(len(data), 2)
        # velocity command will calculate the planned points when a story enters a sprint
        self.assertDictContainsSubset({'planned_points': 3.0, 'carried_points': 0.0, 'completed_points': 0.0}, data[0])
        # velocity command will calculate the carried points when a story is not complete and enters a new sprint
        # velocity command will calculate the completed points when a story is finished in a sprint
        self.assertDictContainsSubset({'planned_points': 0.0, 'carried_points': 3.0, 'completed_points': 3.0}, data[1])

