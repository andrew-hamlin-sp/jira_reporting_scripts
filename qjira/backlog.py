"""
Class encapsulating Backlog calculations. This will 
pivot the issues on fixVersion fields for sorting
between future unreleased versions and dev_backlog,
for example.
"""
from .command import PivotCommand
from .log import Log

class BacklogCommand(PivotCommand):

    @property
    def pivot_field(self):
        return 'fixVersions'

    @property
    def header(self):
        return ['project_key', 'fixVersions_name', 'issuetype_name', 'issue_key',
                'summary', 'priority_name', 'status_name', 'assignee_displayName',
                'created', 'updated', 'severity_value', 'customer']

    @property
    def query(self):
        return 'issuetype = Bug AND resolution = Unresolved ORDER BY priority DESC'
    
    @property
    def count_fields(self):
        return ['customer']

    def retrieve_fields(self, fields):
        return fields + ['priority','created','updated','customfield_10112',
                         'customfield_10400']
