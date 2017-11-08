'''
Summarize the backlog
'''
from operator import itemgetter
from functools import partial

import datetime

from .log import Log
from .command import BaseCommand
from . import jira

# Sprints w/o dates and Issues without sprints
SORT_DEFAULT_YEAR = datetime.date(datetime.MINYEAR, 1, 1)
SORT_REVERSE_YEAR = datetime.date(datetime.MAXYEAR, 1, 1)


def sprint_startDate_sort(x, reverse=False):
    if x.get('sprint_0_name'):
        return x.get('sprint_0_startDate') or SORT_REVERSE_YEAR
    else:
        return SORT_REVERSE_YEAR if reverse else SORT_DEFAULT_YEAR 


def sprint_header(sprint_name, sprint_startDate, sprint_endDate):
    if sprint_name and sprint_startDate and sprint_endDate:
        return '{}  [{} to {}]'.format(sprint_name.upper(),
                                       sprint_startDate,
                                       sprint_endDate)
    elif  sprint_name:
        return '{}'.format(sprint_name.upper())
    else:
        return 'GROOMING'

    
def hyperlink(url, name):
    if not name:
        name = url
    return '=HYPERLINK("{}","{}")'.format(url, name)

def doc_link_marked_new(row, link_col, date_col, mark_if_new=False):
    name = row[link_col].rpartition('/')[2]
    
    if mark_if_new and date_col in row and \
       row[date_col] >= datetime.date.today()+datetime.timedelta(days=-14):
        name = name + " [New]"
        
    return hyperlink(row[link_col], name)

class SummaryCommand(BaseCommand):

    def __init__(self, mark_if_new=False, *args, **kwargs):
        super(SummaryCommand, self).__init__(*args, **kwargs)
        self._mark_if_new = mark_if_new
    
    def _configure_http_request(self):
        return partial(
            super(SummaryCommand, self)._configure_http_request(),
            reverse_sprints=True)
        
    @property
    def header(self):
        return ['issue_link','summary','assignee_displayName','design_doc_link',
                'testplan_doc_link','story_points','status_name','epic_link']

    @property
    def query(self):
        return 'issuetype = Story'

    def retrieve_fields(self, fields):
        return fields + ['customfield_11101', 'customfield_14300']
    
    def _new_row(self):
        return {k:'=T(" ")' for k in self.header}

    # build table of epic links
    def _resolve_epic(self, epic_key):
        username=self.kwargs.get('username')
        password=self.kwargs.get('password')
        epic = jira.get_issue(self._base_url, epic_key,
                              username=username, password=password)
        #print('> resolve_epic: {0}'.format(epic))
        return jira.get_browse_url(self._base_url, epic_key), epic['customfield_10019']
    
    def post_process(self, rows):
        # Secondary sort by issuekey
        rows = sorted(rows, key=itemgetter('issue_key'))
        # Secondary sort by epickey
        rows = sorted(rows, key=lambda x: x.get('epic_issue_key') or '')
        # Secondary sort by name to distinguish grooming sprint from non-started sprints
        rows = sorted(rows, key=lambda x: x.get('sprint_0_name') or '')
        # Primary sort by sprint startdate
        rows = sorted(rows, key=partial(sprint_startDate_sort))
        
        epics = set(row['epic_issue_key'] for row in rows if row.get('epic_issue_key'))
        
        epic_link_table = { epic:self._resolve_epic(epic) for epic in epics }
        
        sprint_placeholder = 'na'
        
        for idx,row in enumerate(rows):
            #print('> post_process enumerate(rows): {0} {1}'.format(idx, row))
            if sprint_placeholder != row.get('sprint_0_name'):
                sprint_placeholder = row.get('sprint_0_name')
                res = self._new_row()
                res.update({
                    'summary': sprint_header(sprint_placeholder, row.get('sprint_0_startDate'), row.get('sprint_0_endDate')),
                })
                yield res
            res = self._new_row()
            epic_key = row.get('epic_issue_key')
            issue_key = row.get('issue_key')
            if epic_key:
                url, name = epic_link_table[epic_key]
                row['epic_link'] = hyperlink(url, name)

            if issue_key:
                row['issue_link'] = hyperlink(jira.get_browse_url(self._base_url, issue_key), issue_key)

            if 'design_doc_link' in row:
                row['design_doc_link'] = doc_link_marked_new(row,
                                                             'design_doc_link',
                                                             'eng_design_changed',
                                                             mark_if_new=self._mark_if_new)

            if 'testplan_doc_link' in row:
                row['testplan_doc_link'] = doc_link_marked_new(row,
                                                               'testplan_doc_link',
                                                               'eng_test_plan_changed',
                                                               mark_if_new=self._mark_if_new)
            
            res.update(row)
            yield res

