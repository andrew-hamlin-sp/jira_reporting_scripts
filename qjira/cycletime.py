'''Class encapsulating cycle time of an issue. This class will
   calculate the days from being moved to In Progress by devs
   to being Closed by testers.

   Limitations: 

   This does not subtract time for an issue
   moved from In Progress back to Open. 

   This does not record separate values for bugs being dev
   complete Resolved and being test complete Closed.
'''
import dateutil.parser
import datetime

from .log import Log
from .data import calculate_rows

class CycleTime:

    def __init__(self, project=[], fixversion=[]):
        # stories and bugs have different status for the endDate: Donen ahd Closed, respectively
        self._header = ['project_key','fixVersions_0_name','issuetype_name','issue_key','story_points','status_InProgress','status_Done', 'status_Closed']
        self._projects = project
        self._fixversions = fixversion

    @property
    def header(self):
        return self._header

    def query(self, callback):
        queries = ['((issuetype = Story AND status in (Done, Accepted)) OR (issuetype = Bug AND status = Closed))']

        if self._fixversions:
            fixversions = ','.join(self._fixversions)
            queries.insert(0, 'fixVersion in ({})'.format(fixversions))

        if self._projects:
            projects = ','.join(self._projects)
            queries.insert(0, 'project in ({})'.format(projects))
        
        callback(' AND '.join(queries))

    def process(self, issues):
        #Log.debug('process ', len(issues))
        results = [row for iss in issues for row in calculate_rows(iss)]
        return results

