#from . import test_context

import sys
PY3 = sys.version_info[0] > 2

import unittest

from . import velocity_tests
from . import cycletime_tests
from . import summary_tests
from . import dataprocessor_tests
from . import main_tests
from . import techdebt_tests
from . import backlog_tests
from . import jira_tests

def suite():
    suite = unittest.TestSuite()

    if PY3:
        from . import log_tests
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(log_tests.LogTest))

    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(jira_tests.TestJira))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(velocity_tests.TestVelocity))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(cycletime_tests.TestCycleTime))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(summary_tests.TestSummary))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(dataprocessor_tests.TestDataProcessor))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(main_tests.TestMainCLI))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(techdebt_tests.TestTechDebt))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(backlog_tests.TestBacklog))
    return suite
    
if __name__ == '__main__':
    testrunner = unittest.TextTestRunner()
    testrunner.run(suite())
    
