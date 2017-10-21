'''Class encapsulating Velocity processing. This will
   calculate the story points planned, completed, and 
   carried over for every sprint associated with an issue.

   Issues (story or bug) that have not been assigned at 
   least one sprint will not be reported on (because velocity
   only makes sense in the context of a sprint(s).

   Sprints without defined start and end dates  will not be reported.

'''
from .command import PivotCommand
from .log import Log

DEFAULT_POINTS = 0.0

class VelocityCommand(PivotCommand):
    '''Analyze data for velocity metrics'''

    def __init__(self, include_bugs=False, forecast=False, *args, **kwargs):
        super(VelocityCommand, self).__init__(*args, **kwargs)
        self._include_bugs = include_bugs
        self._forecast = forecast

    @property
    def pivot_field(self):
        return 'sprint'
        
    @property
    def header(self):
        return  ['project_key','fixVersions_0_name','issuetype_name','issue_key',
                 'sprint_name','sprint_startDate','sprint_endDate','story_points',
                 'planned_points','carried_points','completed_points']

    @property
    def query(self):
        if self._include_bugs:
            return 'issuetype in (Story, Bug)'
        else:
            return 'issuetype = Story'

    def post_process(self, rows):
        '''data processor wrapper to calculate points as planned, carried, completed'''
        last_issue_seen = None
        counter = 0
        for idx,row in enumerate(rows):
            if not self._forecast and not row.get('sprint_completeDate'):
                #print ('> skip incomplete sprint')
                continue

            if row['issue_key'] is not last_issue_seen:
                last_issue_seen = row['issue_key']
                counter = 0
            else:
                counter += 1
            point_value = row.get('story_points', DEFAULT_POINTS)
            planned_points = point_value if counter == 0 else DEFAULT_POINTS
            carried_points = point_value if counter >= 1 else DEFAULT_POINTS
            completed_points = point_value if self._isComplete(row) else DEFAULT_POINTS
            update = {
                'planned_points': planned_points,
                'carried_points': carried_points,
                'completed_points': completed_points
            }
            row.update(update)
            yield row

    def _isComplete(self, row):
        '''Issue is complete when status changed between sprint startDate & endDate'''
        completedDate = row.get('status_Done') \
                        if row['issuetype_name'] == 'Story' \
                        else row.get('status_Closed')
        if not completedDate:
            return False
        
        sprintStartDate = row.get('sprint_startDate')
        sprintCompletionDate = row.get('sprint_completeDate')
        #print('> isComplete start: {0}, completion: {1}, done: {2}'.format(sprintStartDate, sprintCompletionDate, completedDate))
        return sprintCompletionDate and \
            completedDate >= sprintStartDate and \
            completedDate <= sprintCompletionDate
