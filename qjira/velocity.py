'''Class encapsulating Velocity processing'''
import datetime

from .log import Log
from .util import sprint_info

class Velocity:
    '''Analyze data for velocity metrics'''
    
    def __init__(self, project=[], exclude_carryover=False):
        # create dictionary of values
        self._fieldnames = ['project','issue','sprint','startDate','endDate','planned','completed','carried']
        self._projects = project
        self._exclude_carryover = exclude_carryover

    @property
    def header(self):
        return self._fieldnames

    def query(self, callback):
        Log.debug('query')
        callback('project in ({}) AND issuetype in (Story, Bug)'.format(','.join(self._projects)))
    
    def process(self, issues):
        #Log.debug('process ', len(issues))
        for issue in issues:
            for sprint in self._process_story_sprints(issue):
                yield sprint
        
    def _process_story_sprints (self, story):
        '''Extract tuple containing sprint, issuekey, and story points from Story'''
        issuekey = story['key']
        fields = story['fields']
        points = fields['customfield_10109']
        project = fields['project']['key']
        status = fields['status']['name']
        completed = points if (status == 'Done' or status == 'Accepted') else 0
        sprints = story['fields'].get('customfield_10016')

        if sprints:
            infos = sorted([sprint_info(sprint) for sprint in sprints], key=lambda k: k['startDate'])
        else:
            infos = [dict()]

        for idx,info in enumerate(infos):
            isLast = idx == len(infos)-1
            name = info.get('name', None)
            startDate = info.get('startDate', None)
            endDate = info.get('endDate', None)
            yield {
                'project':   project,
                'issue':     issuekey,
                # planned points count all the way through
                'planned':   points if points else 0,
                # completed points only count at the last iteration worked
                'completed': completed if isLast else 0,
                # carried points count after first iteration until completed
                'carried': points if idx > 0 else 0,
                'name' : name if name else '',
                'startDate': startDate.date() if startDate else '',
                'endDate':endDate.date() if endDate else ''
            }
        
            

