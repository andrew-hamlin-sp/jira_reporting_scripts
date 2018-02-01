"""
Class encapsulating Backlog calculations. This will 
pivot the issues on fixVersion fields for sorting
between future unreleased versions and dev_backlog,
for example.
"""

from collections import OrderedDict

from .command import PivotCommand
from .log import Log
from . import headers

class BacklogCommand(PivotCommand):

    @property
    def pivot_field(self):
        return 'fixVersions'

    @property
    def header(self):
        return OrderedDict([headers.get_column('project_key'),
                            headers.get_column('fixVersions_name'),
                            headers.get_column('issuetype_name'),
                            headers.get_column('issue_key'),
                            headers.get_column('summary'),
                            headers.get_column('priority_name'),
                            headers.get_column('status_name'),
                            headers.get_column('assignee_displayName'),
                            headers.get_column('created'),
                            headers.get_column('updated'),
                            headers.get_column('severity_value'),
                            headers.get_column('customer')])
    
    @property
    def query(self):
        return 'issuetype = Bug AND resolution = Unresolved ORDER BY priority DESC'
    
    @property
    def count_fields(self):
        return ['customer']

    def retrieve_fields(self, fields):
        return fields + ['priority','created','updated','customfield_10112',
                         'customfield_10400']
