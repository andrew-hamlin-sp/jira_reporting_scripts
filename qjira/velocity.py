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
from .util import sprint_info, current_status

class Velocity:
    '''Analyze data for velocity metrics'''
    
    def __init__(self, project=[]):
        # create dictionary of values
        self._fieldnames = ['project','issue','sprint','startDate','endDate','planned','completed','carried']
        self._projects = project

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
        
    def _process_story_sprints (self, issue):
        '''Extract tuple containing sprint, issuekey, and story points from Story'''
        issuekey = issue['key']
        fields = issue['fields']
        points = fields['customfield_10109']
        project = fields['project']['key']
        
        status = current_status(issue)
        
        # Bugs do not have a status field
        isCompleted = (status == 'Done' or status == 'Accepted' or status == 'Closed')

        if not points:
            points = 0
        
        #print ('story is complete? {}'.format(isCompleted))
        
        sprints = issue['fields'].get('customfield_10016')
        if sprints is None:
            return

        sprint_infos = sorted([sprint_info(sprint) for sprint in sprints], key=lambda k: k['startDate'])
        # find carry-over points from previous sprint
        # add completed points to last sprint worked


        results = []
        for idx, info in enumerate(sprint_infos):
            if not info['startDate'] or not info['endDate']:
                continue

            name = info['name']           
            startDate = info['startDate'].date()
            endDate = info['endDate'].date()

            results.append({
                'project': project,
                'issue': issuekey,
                'sprint': name,
                'startDate': startDate,
                'endDate': endDate,
                'planned': points if idx < 1 else 0,
                'carried': points if idx > 0 else 0,
                'completed': 0
            })
            
        if results:
            results[-1]['completed'] = points if isCompleted else 0

        for result in results:
            yield result
            

