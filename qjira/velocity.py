'''Class encapsulating Velocity processing. This will
   calculate the story points planned, completed, and 
   carried over for every sprint associated with an issue.

   Issues (story or bug) that have not been assigned at 
   least one sprint will not be reported on (because velocity
   only makes sense in the context of a sprint(s).

   Sprints without defined start and end dates  will not be reported.

'''
import datetime

from .command import Command
from .dataprocessor import DataProcessor
from .log import Log

DEFAULT_POINTS = 0.0

class Velocity(Command):
    '''Analyze data for velocity metrics'''
    
    def __init__(self, *args, **kwargs):
        Command.__init__(self, args, kwargs, processor=DataProcessor(pivot='sprint'))
        self._fieldnames = ['project_key','fixVersions_0_name','issuetype_name','issue_key','sprint_name','sprint_startDate','sprint_endDate','story_points','planned_points','carried_points','completed_points']
        self._query = 'issuetype = Story'
        
    @property
    def header(self):
        return self._fieldnames

    @property
    def query(self):
        return self._query

    def post_process(self, rows):
        '''data processor wrapper to calculate points carried, completed'''
        count = len(rows)
        results = []
        for idx,row in enumerate(rows):
            #print ('> row {} keys= {}'.format(idx+1, row.keys()))
            if not row.get('sprint_completeDate'):
                #print ('skip incomplete sprint')
                continue
            
            point_value = row.get('story_points', DEFAULT_POINTS)
            planned_points = point_value if idx == 0 else DEFAULT_POINTS
            carried_points = point_value if idx >= 1 else DEFAULT_POINTS
            completed_points = point_value if idx == count-1 and self._isComplete(row) else DEFAULT_POINTS
            update = {
                'planned_points': planned_points,
                'carried_points': carried_points,
                'completed_points': completed_points
            }
            row.update(update)
            results.append(row)
        return results

    def _isComplete(self, row):

        if row['issuetype_name'] == 'Story':
            return row.get('status_Done', False)
        elif row['issuetype_name'] == 'Bug':
            return row.get('status_Closed', False)

        return False
