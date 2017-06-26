import test_context

import unittest

from qjira.container import Container

class TestContainer(unittest.TestCase):

    def test_shared_dictionary(self):
        c1 = Container()
        c2 = Container()
        self.assertIs(c1, c2)

        c1['test'] = object()
        self.assertIs(c1['test'], c2['test'])
