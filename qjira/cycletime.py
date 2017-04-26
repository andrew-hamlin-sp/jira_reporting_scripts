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

class CycleTime:

    def __init__(self, project=[]):
        self._header = 'project,issue,points,start,end'
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
        fields = story['fields']
        points = fields['customfield_10109']
        project = fields['project']['key']

        # calculate based on fields['issuetype']['name']
        # Story to 3 (In Progress) and  10001 (Done) 
        # Bug to 3 (In Progress) to 5 (Resolved) and to 6 (Closed)
        # for now, cycletime based on Test complete (6)
        cycle_times = [dateutil.parser.parse(entry['created'])
                       for entry in story['changelog'].get('histories')
                       if entry['items'][0].get('field') == 'status'
                       and (
                           entry['items'][0].get('to') == '3'
                           or entry['items'][0].get('to') == '10001'
                           or entry['items'][0].get('to') == '6'
                       )]

        start_time = datetime.datetime(datetime.MINYEAR, 1, 1)
        end_time = datetime.datetime(datetime.MINYEAR, 1, 1)
        if not cycle_times:
            return
        
        # sort by created date so we can use find first In Progress
        # and last Done status
        sorted_times = sorted(cycle_times)    
        start_time = sorted_times[0]
        end_time = sorted_times[-1]
            
        yield (project,issuekey, points, start_time.date(), end_time.date())

