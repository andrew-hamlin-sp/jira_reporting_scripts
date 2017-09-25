from . import test_context

import unittest
import datetime

import io

import qjira.dataprocessor as dp

from . import test_data

class TestDataProcessor(unittest.TestCase):

    def test_nested_data_flattens(self):
        row = next(dp.flatten_json_struct(test_data.nested_data()))
        [self.assertFalse(type(v)==list, msg='flattened data contains list') 
         for v in row.values()]
        [self.assertFalse(type(v)==dict, msg='flattened data contains dict')
         for v in row.values()]

        
