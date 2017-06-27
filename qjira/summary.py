'''
Summarize the backlog

To Do: replace epic issue key with call back to Jira to retrieve the Epic Name property

'''

from operator import itemgetter
from functools import partial

import datetime
from .log import Log
from .dataprocessor import calculate_rows
from .container import Container

# Sprints w/o dates and Issues without sprints
SORT_DEFAULT_YEAR = datetime.date(datetime.MINYEAR, 1, 1)
SORT_REVERSE_YEAR = datetime.date(datetime.MAXYEAR, 1, 1)

_svc = Container()

# build table of epic links
def resolve_epic(epic_key):
    epic = _svc['jira'].get_issue(epic_key)
    return _svc['jira'].get_browse_url(epic_key), epic['fields']['customfield_10019']

def sprint_startDate_sort(x, reverse=False):
    # Note: using simple dict.get with default value does not work here - unsure why
    if x.get('sprint_0_name'):
        return x.get('sprint_0_startDate') or SORT_REVERSE_YEAR
    else:
        return SORT_REVERSE_YEAR if reverse else SORT_DEFAULT_YEAR 


def sprint_header(sprint_name, sprint_startDate, sprint_endDate):
    if sprint_name and sprint_startDate and sprint_endDate:
        return '{}  [{:%x} to {:%x}]'.format(sprint_name.upper(), sprint_startDate, sprint_endDate)
    elif  sprint_name:
        return '{}'.format(sprint_name.upper())
    else:
        return 'GROOMING'

    
def hyperlink(url, name):
    if not name:
        name = url
    return '=HYPERLINK("{}","{}")'.format(url, name)
    
class Summary:

    def __init__(self, reverse=False):
        self._fieldnames = ['issue_link','summary','assignee_displayName','design_doc_link','testplan_doc_link','story_points','epic_link']
        self._query = 'issuetype = Story'
        self._reverseSort = reverse

    @property
    def header(self):
        return self._fieldnames

    @property
    def query(self):
        return self._query

    def new_row(self):
        return {k:'=T(" ")' for k in self._fieldnames}
    
    def process(self, issues):
        Log.debug('Process {} issues'.format(len(issues)))

        rows = [row for issue in issues for row in calculate_rows(issue, reverse_sprints=True)]
        # Secondary sort by issuekey
        rows = sorted(rows, key=itemgetter('issue_key'))
        # Secondary sort by epickey
        rows = sorted(rows, key=lambda x: x.get('epic_issuekey') or '')
        # Secondary sort by name to distinguish grooming sprint from non-started sprints
        rows = sorted(rows, key=lambda x: x.get('sprint_0_name') or '')
        # Primary sort by sprint startdate
        rows = sorted(rows, key=partial(sprint_startDate_sort, reverse=self._reverseSort), reverse=self._reverseSort)
        
        epics = set(row['epic_issuekey'] for row in rows if row.get('epic_issuekey'))
        
        epic_link_table = { epic:resolve_epic(epic) for epic in epics }
        
        results = []
        sprint_placeholder = 'na'
        
        for idx,row in enumerate(rows):
            if sprint_placeholder != row.get('sprint_0_name'):
                sprint_placeholder = row.get('sprint_0_name')
                res = self.new_row()
                res.update({
                    'summary': sprint_header(sprint_placeholder, row.get('sprint_0_startDate'), row.get('sprint_0_endDate')),
                })
                results.append(res)
            res = self.new_row()
            epic_key = row.get('epic_issuekey')
            issue_key = row.get('issue_key')
            if epic_key:
                epic_link = epic_link_table[epic_key]
                row['epic_link'] = hyperlink(*epic_link)

            if issue_key:
                row['issue_link'] = hyperlink(_svc['jira'].get_browse_url(issue_key), issue_key)

            for L in ['design_doc_link','testplan_doc_link']:
                if row.get(L):
                    row[L] = hyperlink(row[L], row[L].rpartition('/')[2])
            res.update(row)
            results.append(res)
        return results
