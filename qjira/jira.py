'''Executes simple queries of Jira Cloud REST API'''

import requests
import json

from urllib.parse import urlencode
#from requests.auth import HTTPBasicAuth


from .log import Log

class Jira:

    # constants
    ISSUE_ENDPOINT='https://{}/rest/api/2/issue/{}?{}'

    ISSUE_SEARCH_ENDPOINT='https://{}/rest/api/2/search?{}'
    
    HEADERS = {'content-type': 'application/json'}

    # expands the changelog of each issue and hides all but essential fields
    # customfield 10109 is the 'story points' field
    # customfield 10016 is the 'iteration' or 'sprint' field, an array
    QUERY_STRING_DICT = {
        'expand': 'changelog',
        'fields': '-*navigable,customfield_10109,customfield_10016'
    }
            
    def __init__ (self, baseUrl, **kwargs):
        ''' Construct new Jira client '''
        self.baseUrl = baseUrl
        for k in ('username', 'password', 'auth'):
            setattr(self, k, kwargs.get(k))

        #self.auth=HTTPBasicAuth(self.username, self.password)

    # def get_issues (self, issues):
    #     '''Generator returning json of all issues'''

    #     search_args = Jira.QUERY_STRING_DICT.copy()
    #     query_string = urlencode(search_args)
        
    #     for n in issues:
    #         url = Jira.ISSUE_ENDPOINT.format(self.baseUrl, n, query_string)
    #         Log.debug(url)

    #         # retrieve parent
    #         r = requests.get(url, auth=(self.username, self.password), headers=Jira.HEADERS)
    #         Log.debug(r.status_code)
            
    #         # TODO assert issuetype is story
    #         r.raise_for_status()

    #         json = r.json()

    #         yield json

    def get_project_issues (self, query_callback):
        '''Perform a JQL search across `projects` and return issues'''

        Log.debug('get_project_issues')
        search_args = Jira.QUERY_STRING_DICT.copy()
        
        query_callback(lambda jql: search_args.update({'jql':jql}))

        query_string = urlencode(search_args)        
        url = Jira.ISSUE_SEARCH_ENDPOINT.format(self.baseUrl, query_string)
        Log.debug('url = ' + url)

        r = requests.get(url, auth=(self.username, self.password), headers=Jira.HEADERS)

        Log.debug(r.status_code)
        r.raise_for_status()

        json = r.json()

        # return and process each issue
        return json['issues']

