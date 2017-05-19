'''
Summarize the backlog

To Do: replace epic issue key with call back to Jira to retrieve the Epic Name property

'''

from operator import itemgetter
from functools import partial

import datetime
from .log import Log
from .dataprocessor import calculate_rows

# Sprints w/o dates and Issues without sprints
SORT_DEFAULT_YEAR = datetime.date(datetime.MINYEAR, 1, 1)
SORT_REVERSE_YEAR = datetime.date(datetime.MAXYEAR, 1, 1)

def sprint_startDate_sort(x, reverse=False):
    # Note: using simple dict.get with default value does not work here - unsure why
    if x.get('sprint_0_name'):
        return x.get('sprint_0_startDate') or SORT_REVERSE_YEAR
    else:
        return SORT_REVERSE_YEAR if reverse else SORT_DEFAULT_YEAR 

def hyperlink(url, name):
    if not name:
        name = url
    return '=HYPERLINK("{}","{}")'.format(url, name)
    
class Summary:

    def __init__(self, jira, reverse=False):
        self._fieldnames = ['issue_link','summary','design_doc_link','testplan_doc_link','story_points','epic_link']
        self._query = 'issuetype = Story'
        self._reverseSort = reverse
        self._jira = jira

    @property
    def header(self):
        return self._fieldnames

    @property
    def query(self):
        return self._query

    def process(self, query_string):
        
        issues = self._jira.get_project_issues(query_string)
        Log.debug('Process {} issues'.format(len(issues)))

        rows = [row for issue in issues for row in calculate_rows(issue)]
        # Secondary sort by issuekey
        rows = sorted(rows, key=itemgetter('issue_key'))
        # Secondary sort by epickey
        rows = sorted(rows, key=lambda x: x.get('epic_issuekey') or '')
        # Secondary sort by name to distinguish grooming sprint from non-started sprints
        rows = sorted(rows, key=lambda x: x.get('sprint_0_name') or '')
        # Primary sort by sprint startdate
        rows = sorted(rows, key=partial(sprint_startDate_sort, reverse=self._reverseSort), reverse=self._reverseSort)

        def sprint_header(sprint_name, sprint_startDate):
            if sprint_placeholder:
                return '{} (started: {})'.format(sprint_name, sprint_startDate or 'Not started')
            return 'GROOMING'
        
        # build table of epic links
        def resolve_epic(epic_key):
            epic = self._jira.get_issue(epic_key)
            return self._jira.get_browse_url(epic_key), epic['fields']['customfield_10019']
        
        epics = set(row['epic_issuekey'] for row in rows if row.get('epic_issuekey'))
        epic_link_table = { epic:resolve_epic(epic) for epic in epics }
        
        results = []
        sprint_placeholder = 'na'

        for idx,row in enumerate(rows):
            if sprint_placeholder != row.get('sprint_0_name'):
                sprint_placeholder = row.get('sprint_0_name')
                results.append({
                    'summary': sprint_header(sprint_placeholder, row.get('sprint_0_startDate')),
                })
            res = {k:'n/a' for k in self._fieldnames}
            epic_key = row.get('epic_issuekey')
            if epic_key:
                epic_link = epic_link_table[epic_key]
                row['epic_link'] = hyperlink(*epic_link)
            
            row['issue_link'] = hyperlink(self._jira.get_browse_url(row['issue_key']), row['issue_key'])
            for L in ['design_doc_link','testplan_doc_link']:
                if row.get(L):
                    row[L] = hyperlink(row[L], row[L].rpartition('/')[2])
            res.update(row)
            results.append(res)
        return results
