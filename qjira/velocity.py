'''Class encapsulating Velocity processing'''
import datetime

from .log import Log
from .util import sprint_info

class Velocity:
    def __init__(self, project=[]):
        self._header = 'issue,points,sprint,startDate,endDate'
        self._projects = project

    @property
    def header(self):
        return self._header

    def query(self, callback):
        Log.debug('query')
        callback('project in ({}) AND issuetype = Story'.format(','.join(self._projects)))
    
    def process(self, issues):
        Log.debug('process ', len(issues))
        for issue in issues:
            for sprint in self._process_story_sprints(issue):
                yield sprint
        
    def _process_story_sprints (self, story):
        '''Extract tuple containing sprint, issuekey, and story points from Story'''
        issuekey = story['key']
        points = story['fields'].get('customfield_10109')
        if not points:
            points = 0.0

        sprints = story['fields'].get('customfield_10016')
        if sprints is None:
            yield (issuekey, points,'','','')
            return
       
        # Jira returns list of Sprints as an array of strings that are Java object
        infos = sorted([sprint_info(sprint) for sprint in sprints], key=lambda k: k['startDate'])
        for info in infos:
            yield (issuekey, points, info['name'], info['startDate'].date(), info['endDate'].date())

