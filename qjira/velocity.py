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

DEFAULT_POINTS = 0.0

class Velocity:
    '''Analyze data for velocity metrics'''
    
    def __init__(self):
        # NOTE velocity metrics may want to calculate points as planned vs. carried-over vs completed
        self._fieldnames = ['project_key','fixVersions_0_name','issuetype_name','issue_key','sprint_name','sprint_startDate','sprint_endDate','story_points','planned_points','carried_points','completed_points']
        self._query = 'issuetype in (Story, Bug)'
        
    @property
    def header(self):
        return self._fieldnames

    @property
    def query(self):
        return self._query
    
    def process(self, issues):
        #Log.debug('process ', len(issues))
        results = [row for iss in issues for row in self._velocity_row_extras(iss)]
        return results

    def _velocity_row_extras(self, issue):
        '''data processor wrapper to calculate points carried, completed'''
        rows = calculate_rows(issue, pivot='sprint')
        count = len(rows)
        
        for idx,row in enumerate(rows):
            #print ('> row {} of {}'.format(idx+1, count))
            point_value = row.get('story_points', DEFAULT_POINTS)
            planned_points = point_value if idx == 0 else DEFAULT_POINTS
            carried_points = point_value if idx >= 1 else DEFAULT_POINTS
            completed_points = point_value if idx == count-1 else DEFAULT_POINTS
            update = {
                'planned_points': planned_points,
                'carried_points': carried_points,
                'completed_points': completed_points
            }
            #print ('> updated {}'.format(update))
            row.update(update)
            yield row

        
