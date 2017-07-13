import test_context

import unittest
import datetime

import log_tests
import velocity_tests
import cycletime_tests
import summary_tests
import dataprocessor_tests
import main_tests

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(log_tests.LogTest))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(velocity_tests.TestVelocity))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(cycletime_tests.TestCycleTime))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(summary_tests.TestSummary))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(dataprocessor_tests.TestDataProcessor))            
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(main_tests.TestMainCLI))
    return suite
    
if __name__ == '__main__':
    testrunner = unittest.TextTestRunner()
    testrunner.run(suite())
    
