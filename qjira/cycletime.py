'''Class encapsulating cycle time of an issue. This class will
   calculate the days from being moved to In Progress by devs
   to being Closed by testers. Results are sorted by start and
   end dates, oldest to newest.

   Limitations: 

   This does not subtract time for an issue
   moved from In Progress back to Open. 

   This does not record separate values for bugs being dev
   complete Resolved and being test complete Closed.
'''
import dateutil.parser
import datetime
from operator import itemgetter

from .log import Log
from .dataprocessor import calculate_rows

def networkdays(start, end):
    return '=NETWORKDAYS("{}","{}")'.format(start, end)

class CycleTime:

    def __init__(self):
        self._header = ['project_key','fixVersions_0_name','issuetype_name','issue_key','story_points','status_InProgress','status_Done', 'count_days']
        self._query = 'issuetype = Story AND status in (Done, Accepted)'
        
    @property
    def header(self):
        return self._header

    @property
    def query(self):
        return self._query
        
    def process(self, issues):
        Log.debug('Process {} issues'.format(len(issues)))
        results = [row for iss in issues for row in self._processing(calculate_rows(iss))]
        results = sorted(results, key=itemgetter('status_Done'))
        results = sorted(results, key=itemgetter('status_InProgress'))
        return results

    def _processing(self, rows):
        for row in rows:
            if not row.get('story_points'):
                continue

            # if finished without progress, then cycletime = 0
            if not row.get('status_InProgress'):
                row['status_InProgress'] = row['status_Done']

            # allow Excel to produce count of workdays
            row['count_days'] = networkdays(row['status_InProgress'], row['status_Done'])
                
            yield row
            
