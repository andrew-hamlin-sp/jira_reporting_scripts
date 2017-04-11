#!bin/python

'''
cycle_times.py

Author: Andrew Hamlin

Description: A command line tool to export changelog history using Jira Cloud REST API. The
goal is to correlate the estimated cycle time with the estimated story points assigned.

'''

import sys
import argparse
import getpass
import dateutil.parser
import datetime

# project imports
from log import Log
from jira import Jira

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
