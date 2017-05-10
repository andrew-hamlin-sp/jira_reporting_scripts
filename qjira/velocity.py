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
from .data import calculate_rows

class Velocity:
    '''Analyze data for velocity metrics'''
    
    def __init__(self, project=[], fixversion=[]):
        # NOTE velocity metrics may want to calculate points as planned vs. carried-over vs completed
        self._fieldnames = ['project_key','fixVersions_0_name','issuetype_name','issue_key','sprint_name','sprint_startDate','sprint_endDate','story_points']
        self._projects = project
        self._fixversions = fixversion

    @property
    def header(self):
        return self._fieldnames

    def query(self, callback):
        queries = ['issuetype in (Story, Bug)']

        if self._fixversions:
            fixversions = ','.join(self._fixversions)
            Log.debug('fixversions = ' + fixversions)
            queries.insert(0, 'fixVersion in ({})'.format(fixversions))

        if self._projects:
            projects = ','.join(self._projects)
            Log.debug('projects = ' + projects)
            queries.insert(0, 'project in ({})'.format(projects))
        
        callback(' AND '.join(queries))
    
    def process(self, issues):
        #Log.debug('process ', len(issues))
        results = [row for iss in issues for row in calculate_rows(iss, pivot='sprint')]
        return results
