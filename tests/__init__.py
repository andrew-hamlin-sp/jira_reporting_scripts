"""Test module for qjira"""
import unittest

from . import velocity_tests
from . import cycletime_tests
from . import summary_tests
from . import techdebt_tests
from . import backlog_tests
from . import jira_tests
from . import log_tests
from . import main_tests    
from . import unicode_csv_writer_tests
from . import jql_tests

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(jira_tests.TestJiraFunc))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(velocity_tests.TestVelocity))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(velocity_tests.TestVelocityWithBugs))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(cycletime_tests.TestCycleTime))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(summary_tests.TestSummary))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(techdebt_tests.TestTechDebt))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(backlog_tests.TestBacklog))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(unicode_csv_writer_tests.TestUnicodeWriter))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(unicode_csv_writer_tests.TestAllFields))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(log_tests.LogTest))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(main_tests.TestMainCLI))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(jql_tests.TestJQLCommand))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(jql_tests.TestJQLCommandWithAdditionalFieldsColumns))
    
    return suite
    
if __name__ == '__main__':
    testrunner = unittest.TextTestRunner()
    testrunner.run(suite())
    
