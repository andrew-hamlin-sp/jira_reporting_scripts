'''
Analyze tech debt ratios Story vs Bug points.
'''
from functools import partial, cmp_to_key, reduce as reduce_
from collections import OrderedDict

from .command import BaseCommand
from .log import Log
from . import headers

DEFAULT_POINTS = 0.0
TOTAL_COL = 'Grand Total'

class TechDebtCommand(BaseCommand):

    @property
    def header(self):
        return OrderedDict([headers.get_column('project_name'),
                            headers.get_column('bug_points'),
                            headers.get_column('story_points'),
                            headers.get_column('tech_debt')])

    @property
    def query(self):
        return 'issuetype in (Story, Bug) AND status in (Accepted, Closed, Done)'

    def _format_points(self, f):
        return '{:.0f}'.format(f)

    def _tech_debt_perc(self, val):
        '''Calculate percentage of tuple (bug,story)'''
        try:
            return '{:.0f}%'.format(100 * (val[0] / ( val[0] + val[1] )))
        except ZeroDivisionError:
            return '{:.0f}%'.format(0)

    def _to_story_points(self, x, y):
        '''Accumulate all points of same type into a new structure.

        x is new structure: {project_name: tuple}
        y is source row
        '''
        proj_name = y['project_name']
        story_points = y.get('story_points') or 0
        
        if y['issuetype_name'] == 'Story':
            item = (0, story_points)
        else:
            item = (story_points, 0)

        if proj_name in x:
            x[proj_name] = tuple(map(sum, zip(x[proj_name], item)))
        else:
            x[proj_name] = item

        if TOTAL_COL not in x:
            x[TOTAL_COL] = (0,0)
            
        x[TOTAL_COL] = tuple(map(sum, zip(x[TOTAL_COL], item)))
        return x

    def _sort_by_name(self, name, x, y):
        '''Sort dict by key name.

        Always sort TOTAL_COL at the end.
        '''
        if x[name] == TOTAL_COL:
            return 1
        elif y[name] == TOTAL_COL:
            return -1
        else:
            lx = x[name].lower()
            ly =y[name].lower()
            return (lx > ly) - (lx < ly)
    
    def post_process(self, rows):
        """
        Build a table including:
        Project name | Bug pts | Story pts | Debt %
        Name1        |
        NameN        |
        Grand Total  |
        """
        project_points_by_type = reduce_(self._to_story_points, rows, {})
        results = ({
            'project_name': k,
            'bug_points': self._format_points(v[0]),
            'story_points': self._format_points(v[1]),
            'tech_debt': self._tech_debt_perc(v)
        } for k, v in project_points_by_type.items())
        sort_by_name = partial(self._sort_by_name, 'project_name')
        return sorted(results, key=cmp_to_key(sort_by_name))
    
