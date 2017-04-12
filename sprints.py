#!bin/python
'''
sprints.py

Author: Andrew Hamlin

Description: A command line tool to export data using Jira Cloud REST API. The goal
is to flatten exported data by iterations (sprint).
'''

import sys
import argparse
import re
import getpass

# project imports
from log import Log
from jira import Jira

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

