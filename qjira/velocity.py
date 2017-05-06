'''Class encapsulating Velocity processing. This will
   calculate the story points planned, completed, and 
   carried over for every sprint associated with an issue.

   Issues (story or bug) that have not been assigned at 
   least one sprint will not be reported on (because velocity
   only makes sense in the context of a sprint(s).

   Sprints without defined start and end dates  will not be reported.

'''
import datetime

from .log import Log
from .data import DataProcessor

class Velocity:
    '''Analyze data for velocity metrics'''
    
    def __init__(self, project=[]):
        # NOTE velocity metrics may want to calculate points as planned vs. carried-over vs completed
        self._fieldnames = ['project_key','issuetype_name','issue_key','sprint_name','sprint_startDate','sprint_endDate','story_points']
        self._projects = project

    @property
    def header(self):
        return self._fieldnames

    def query(self, callback):
        Log.debug('query')
        callback('project in ({}) AND issuetype in (Story, Bug)'.format(','.join(self._projects)))
    
    def process(self, issues):
        #Log.debug('process ', len(issues))
        results = [row for iss in issues for row in DataProcessor(iss, pivot='sprint').rows()]
        return results
