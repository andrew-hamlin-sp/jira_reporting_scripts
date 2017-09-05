"""
Class encapsulating Backlog calculations. This will 
pivot the issues on fixVersion fields for sorting
between future unreleased versions and dev_backlog,
for example.
"""

from .command import Command
from .dataprocessor import DataProcessor
from .log import Log

from .jira import Jira

class Backlog(Command):

    def __init__(self, *args, **kwargs):
        Command.__init__(self, *args, processor=DataProcessor(pivot='fixVersions', count_fields=['customer']), **kwargs)

        # add additional nav fields
        fields = Jira.QUERY_STRING_DICT['fields']
        Jira.QUERY_STRING_DICT.update({
            'fields': fields + ',priority,created,updated,customfield_10112,customfield_10400'
        })
        
        self._fieldnames = ['project_key', 'fixVersions_name', 'issuetype_name', 'issue_key', 'summary', 'priority_name', 'status_name', 'assignee_displayName', 'created', 'updated','severity_value', 'customer']
        self._query = 'issuetype = Bug AND resolution = Unresolved ORDER BY priority DESC'

    @property
    def header(self):
        return self._fieldnames

    @property
    def query(self):
        return self._query

    def post_process(self, rows):
        return rows
