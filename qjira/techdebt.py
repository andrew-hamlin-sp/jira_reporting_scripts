'''
Analyze tech debt ratios Story vs Bug points.
'''

from operator import itemgetter
#from .dataprocessor import calculate_rows

from .command import Command
from .log import Log

class TechDebt(Command):

    def __init__(self, *args, **kwargs):
        Command.__init__(self, args, kwargs)
        self._fieldnames = [ 'project_name', 'bug_points', 'story_points', 'tech_debt' ]
        self._query = 'issuetype in (Story, Bug) AND status in (Accepted, Closed, Done)'

    @property
    def header(self):
        return self._fieldnames

    @property
    def query(self):
        return self._query
    
    def post_process(self, rows):
        """
        Build a table including:
        Project name | Bug pts | Story pts | Debt %
        Name1        |
        NameN        |
        Grand total  |
        """
        def _tech_debt_perc(val):
            return '{:.0f}%'.format(100 * (val[0] / ( val[0] + val[1] )))

        def _map_proj_name(x):
            """map a row to dict { proj_name: (bug, story) }"""
            proj_name = x['project_name']
            story_points = x.get('story_points', 0)
            if x['issuetype_name'] == 'Story':
                return { x['project_name']: (0, story_points) }
            elif x['issuetype_name'] == 'Bug':
                return { x['project_name']: (story_points, 0) }
            else:
                Log.error('Unknown issuetype_name: %s', x['issuetype_name'])
            return None

        def _format_points(f):
            return '{:.0f}'.format(f)
        
        tmp = {}
        bug_total = 0
        story_total = 0

        for x in map(_map_proj_name, rows):
            for k,v in x.items():
                val = tmp.setdefault(k, (0, 0))              
                tmp[k] = (val[0] + v[0], val[1] + v[1])
                bug_total += v[0]
                story_total += v[1]

        techdebtbyproj = []
        for k, v in tmp.items():
            techdebtbyproj.append({'project_name': k
                                   , 'bug_points': _format_points(v[0])
                                   , 'story_points': _format_points(v[1])
                                   , 'tech_debt': _tech_debt_perc(v)
            })

        sorted_list = sorted(techdebtbyproj, key=itemgetter('project_name'))
        
        # Grand total
        sorted_list.append({'project_name': 'Grand Total'
                            , 'bug_points': _format_points(bug_total)
                            , 'story_points': _format_points(story_total)
                            , 'tech_debt': _tech_debt_perc( (bug_total, story_total) )
        })
        
        return sorted_list
    
