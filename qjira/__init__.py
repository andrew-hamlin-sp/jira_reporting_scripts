
from __future__ import print_function
import sys
import requests
import json
import dateutil.parser
import datetime
import re

from urllib.parse import urlencode
from requests.auth import HTTPBasicAuth


class Log:
    '''Simple logger'''

    # globals
    debugLevel = 0
    
    
    def eprint (*args, **kwargs):
        '''print args to stderr'''
        print(*args, file=sys.stderr, **kwargs)
        
    eprint = eprint

    def error (*msg):
        '''Log as an error'''
        Log.eprint('[ERROR]', *msg)

    error = staticmethod(error)
        
    def info (*msg):
        '''Log message when debug >= 0'''
        if Log.debugLevel < 0:
            return
        Log.eprint('[INFO]', *msg)

    info = staticmethod(info)

    def debug (*msg):
        '''Log message when debug >= 1'''
        if Log.debugLevel < 1:
            return
        Log.eprint('[DEBUG]', *msg)

    debug = staticmethod(debug)
        
    def verbose (*msg):
        '''Log message when debug >= 2'''
        if Log.debugLevel < 2:
            return
        Log.eprint('[VERBOSE]', *msg)

    verbose = staticmethod(verbose)


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

    def get_issues (self, issues):
        '''Generator returning json of all issues'''

        search_args = Jira.QUERY_STRING_DICT.copy()
        query_string = urlencode(search_args)
        
        for n in issues:
            url = Jira.ISSUE_ENDPOINT.format(self.baseUrl, n, query_string)
            Log.debug(url)

            # retrieve parent
            r = requests.get(url, auth=(self.username, self.password), headers=Jira.HEADERS)
            Log.debug(r.status_code)
            
            # TODO assert issuetype is story
            r.raise_for_status()

            json = r.json()

            yield json

    def get_project_issues (self, jql):
        '''Perform a JQL search across `projects` and return issues'''
        
        search_args = Jira.QUERY_STRING_DICT.copy()
        search_args.update({
            'jql': jql
        })
        query_string = urlencode(search_args)
        
        url = Jira.ISSUE_SEARCH_ENDPOINT.format(self.baseUrl, query_string)
        Log.debug(url)

        r = requests.get(url, auth=(self.username, self.password), headers=Jira.HEADERS)

        Log.debug(r.status_code)
        r.raise_for_status()

        json = r.json()

        # return and process each issue
        return json['issues']


class CycleTime:

    def __init__(self, args, jira):
        self._header = 'issue,points,start,end'
        self._jira = jira
        projects = ', '.join(args.project)
        self._jql = 'project in ({}) AND issuetype = Story AND status in (Done, Accepted)'.format(projects)
        pass

    @property
    def header(self):
        return self._header

    def process(self):
        for issue in self._jira.get_project_issues(self._jql):
            for cycle in process_story_cycle_times(issue):
                yield cycle
            
def process_story_cycle_times (story):
    '''Extract tuple containing issuekey, story points, and cycle time from Story'''
    issuekey = story['key']
    points = story['fields'].get('customfield_10109')
                  
    cycle_times = [dateutil.parser.parse(entry['created'])
                   for entry in story['changelog'].get('histories')
                   if entry['items'][0].get('field') == 'status'
                   and (
                       entry['items'][0].get('to') == '3'
                       or  entry['items'][0].get('to') == '10001'
                   )]

    start_time = datetime.datetime(datetime.MINYEAR, 1, 1)
    end_time = datetime.datetime(datetime.MINYEAR, 1, 1)
    if cycle_times:
        # sort by created date so we can use find first In Progress and last Done status
        sorted_times = sorted(cycle_times)
        #print(sorted_times)
    
        start_time = sorted_times[0]
        end_time = sorted_times[-1]
        #    delta = end_time - start_time
            
    yield (issuekey, points, start_time.date(), end_time.date())
    return

class Velocity:
    def __init__(self, args, jira):
        self._header = 'issue,points,sprint'
        self._jira = jira
        projects = ', '.join(args.project)
        self._jql = 'project in ({}) AND issuetype = Story'.format(projects)


    @property
    def header(self):
        return self._header

    def process(self):
        for issue in self._jira.get_project_issues(self._jql):
            for sprint in process_story_sprints(issue):
                yield sprint

def sprint_info (sprint):
    '''Return object from string representation: 'com.atlassian.greenhopper.service.sprint.Sprint@be7f5f[id=82,rapidViewId=52,state=CLOSED,name=Chambers Sprint 9,goal=<null>,startDate=2016-04-25T10:44:22.273-05:00,endDate=2016-05-09T10:44:00.000-05:00,completeDate=2016-05-09T10:48:04.212-05:00,sequence=82]'
    '''
    m = re.search('\[(.+)\]', sprint)
    if m:
        return dict(e.split('=') for e in m.group(1).split(','))
    return None

def process_story_sprints (story):
    '''Extract tuple containing sprint, issuekey, and story points from Story'''
    issuekey = story['key']
    points = story['fields'].get('customfield_10109')
    if not points:
        points = 0.0

    sprints = story['fields'].get('customfield_10016')

    if sprints is None:
       yield (issuekey, points,'')
       return
       
    # Jira returns list of Sprints as an array of strings that are Java object
    infos = [sprint_info(sprint) for sprint in sprints]

    for info in infos:
        yield (issuekey, points, info['name'])

