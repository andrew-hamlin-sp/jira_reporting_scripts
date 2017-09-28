import sys
import copy
from functools import partial

from requests.exceptions import HTTPError
from requests import Response

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

import qjira.jira as _jira

PY3 = sys.version_info > (3,)

class SPTestCase(object):

    def assertRegex_(self, a, re):
        if PY3:
            self.assertRegex(a, re)
        else:
            self.assertRegex_ = self.assertRegexpMatches

    def assertNotRegex_(self, a, re):
        if PY3:
            self.assertNotRegex(a, re)
        else:
            self.assertNotRegexpMatches(a, re)

class MockJira(object):
    '''Mixin for mocking calls to jira.py.

    This class assumes (and is only valid) as a Mixin to a unittest.TestCase. 
    See the assumption that self accesses the assert methods.
    '''

    def setup_mock_jira(self):
        self._original_get_json = _jira._get_json
        _jira._get_json = self.get_json
        self._json_response = {'total': 0, 'issues': []}
        self._raise401 = False
 
    def teardown_mock_jira(self):
        _jira._get_json = self._original_get_json
        self._actual_url = None
        
    def get_json(self, url, *args, **kwargs):
        '''Returns a JSON payload.

        Given a generator expression, this will return each next payload.

        Example:
        json_response = (r for r in [{...}, {...}])
        '''
        self._actual_url = url
        if self.raise401:
            response = Response()
            response.status_code = 401
            raise HTTPError(response=response)

        if isgenerator(self.json_response):
            return next(self.json_response)
        else:
            return self.json_response

    def get_json_response(self):
        return self._json_response

    def set_json_response(self, res):
        self._json_response = res

    def del_json_response(self):
        del self._json_response

    json_response = property(get_json_response,
                             set_json_response,
                             del_json_response,
                             'JSON response for tests')
    @property
    def actual_url(self):
        '''Url passed to jira._get_json'''
        return self._actual_url

    def get_raise401(self):
        return self._raise401

    def set_raise401(self, b):
        self._raise401 = b

    def del_raise401(self):
        del self._raise401

    raise401 = property(get_raise401,
                        set_raise401,
                        del_raise401,
                        'Raise Unauthorized 401 error')
    
    def assertUrlPartsEqual(self, expectedUrl, actualUrl):
        expected_parts = urlparse(expectedUrl)
        actual_parts = urlparse(actualUrl)
        self.assertEqual(expected_parts.path, actual_parts.path)
        expected_qs = parse_qs(expected_parts.query)
        actual_qs = parse_qs(actual_parts.query)
        self.assertEqual(expected_qs.keys(), actual_qs.keys())
        for key in expected_qs.keys():
            expected_list = _build_list(expected_qs[key])
            actual_list = _build_list(actual_qs[key])
            self.assertListEqual(expected_list, actual_list)

def _build_list(list_of_lists):
    result = []
    for s in list_of_lists:
        result += s.split(',')
    return sorted(result)

def isgenerator(iterable):
    if hasattr(iterable, '__iter__') and not hasattr(iterable, '__len__'):
        return True
    else:
        return False
