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
from .util import find_status_history, get_issuetype

class CycleTime:

    def __init__(self, project=[]):
        self._header = ['project','issuetype','issue','points','startDate','endDate']
        self._projects = project

    @property
    def header(self):
        return self._header

    def query(self, callback):
        Log.debug('query')
        callback('project in ({}) AND ((issuetype = Story AND status in (Done, Accepted)) OR (issuetype = Bug AND status = Closed))'.format(','.join(self._projects)))

    def process(self, issues):
        #Log.debug('process ', len(issues))
        for issue in issues:
            for cycletime in self._process_story_cycle_times(issue):
                yield cycletime
            
    def _process_story_cycle_times (self, story):
        '''Extract tuple containing issuekey, story points, and cycle time from Story'''
        issuekey = story['key']
        issuetype = get_issuetype(story)
        fields = story['fields']
        points = fields['customfield_10109']
        project = fields['project']['key']

        start_history = find_status_history(story, 'In Progress')
        if issuetype == 'Story':
            end_history = find_status_history(story, 'Done')
        else:
            end_history = find_status_history(story, 'Closed')

        start_time = dateutil.parser.parse(start_history[0]['created']).date() if start_history else None

        end_time = dateutil.parser.parse(end_history[-1]['created']).date() if end_history else None

        # only items with complete date ranges can be calculated
        if not start_time or not end_time:
            return
        
        yield {
            'project': project,
            'issuetype': issuetype,
            'issue': issuekey,
            'points': points,
            'startDate': start_time,
            'endDate': end_time
        }

