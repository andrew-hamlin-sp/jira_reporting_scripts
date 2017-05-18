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
from .dataprocessor import calculate_rows

class CycleTime:

    def __init__(self):
        # stories and bugs have different status for the endDate: Donen ahd Closed, respectively
        self._header = ['project_key','fixVersions_0_name','issuetype_name','issue_key','story_points','status_InProgress','status_End']
        self._query = '((issuetype = Story AND status in (Done, Accepted)) OR (issuetype = Bug AND status = Closed))'
        
    @property
    def header(self):
        return self._header

    @property
    def query(self):
        return self._query
        
    def process(self, issues):
        #Log.debug('process ', len(issues))
        results = [row for iss in issues for row in self._cycletime_processing(iss)]
        return results

    def _cycletime_processing(self, issue):

#          map(self._cycletime_totals, calculate_rows(iss)) if row['story_points']
        rows = calculate_rows(issue)

        for row in rows:
            if not row.get('story_points'):
                continue
            
            row['status_End'] = row['status_Done'] if row.get('status_Done') else row['status_Closed']
            # if finished without progress, then cycletime = 0
            if not row.get('status_InProgress'):
                row['status_InProgress'] = row['status_End']

            yield row
            
