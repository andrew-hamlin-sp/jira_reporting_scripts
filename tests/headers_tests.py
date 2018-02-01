from . import test_context
import unittest

import qjira.headers

class TestHeaders(unittest.TestCase):

    def test_get_column(self):
        self.assertTupleEqual(('project_key', 'Project'), qjira.headers.get_column('project_key'))
        
