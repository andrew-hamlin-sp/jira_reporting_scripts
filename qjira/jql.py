from .command import BaseCommand

from . import jira

class JQLCommand(BaseCommand):

    DEFAULT_COLUMN_NAMES = ['project_key', 'issue_key', 'issuetype_name', 'summary',
                            'status_name', 'assignee_name', 'sprint_0_name',
                            'fixVersions_0_name']
    
    def __init__(self, jql=None, field=None, column=None, *args, **kwargs):
        super(JQLCommand, self).__init__(*args, **kwargs)

        if not jql:
            raise TypeError('Missing keyword "jql"')

        self._jql = jql
        self._fields = field

        if column and len(column)>0:
            self._columns = JQLCommand.DEFAULT_COLUMN_NAMES + column
        else:
            self._columns = JQLCommand.DEFAULT_COLUMN_NAMES
            
    @property
    def header(self):
        '''JQL command returns all fields.
        '''
        return self._columns
    
    @property
    def query(self):
        '''Return the user-provided JQL query'''
        return self._jql

    def retrieve_fields(self, fields):
        if self._fields and len(self._fields)>0:
            return fields + self._fields
        else:
            return fields