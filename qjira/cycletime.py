'''Class encapsulating cycle times'''
import dateutil.parser
import datetime

from .log import Log

class CycleTime:

    def __init__(self, project=[]):
        self._header = 'issue,points,start,end'
        self._projects = project

    @property
    def header(self):
        return self._header

    def query(self, callback):
        Log.debug('query')
        callback('project in ({}) AND issuetype = Story AND status in (Done, Accepted)'.format(','.join(self._projects)))

    def process(self, issues):
        Log.debug('process ', len(issues))
        for issue in issues:
            yield self._process_story_cycle_times(issue)
            
    def _process_story_cycle_times (self, story):
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
            # sort by created date so we can use find first In Progress
            # and last Done status
            sorted_times = sorted(cycle_times)    
            start_time = sorted_times[0]
            end_time = sorted_times[-1]
            
            return (issuekey, points, start_time.date(), end_time.date())
