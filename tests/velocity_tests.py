import test_context

import unittest

from qjira.velocity import Velocity

import test_data

class TestVelocity(unittest.TestCase):

    def setUp(self):
        self.processor = Velocity(None)

    def test_header(self):
        self.assertIsInstance(self.processor.header, list)

    def test_query(self):
        self.assertEquals('issuetype in (Story, Bug)', self.processor.query)

    @unittest.skip('Not implemented')
    def test_process(self):
        pass
