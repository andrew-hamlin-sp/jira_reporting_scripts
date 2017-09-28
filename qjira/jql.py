from .command import BaseCommand

from . import jira

class JQLCommand(BaseCommand):

    def __init__(self, jql=None, *args, **kwargs):
        super(JQLCommand, self).__init__(*args, **kwargs)

        if not jql:
            raise TypeError('Missing keyword "jql"')

        self._jql = jql
        #self._all_fields = True
        
    @property
    def header(self):
        '''JQL command returns all fields.
        '''
        return ['project_key', 'issue_key', 'issuetype_name', 'summary',
                'status_name', 'assignee_name', 'sprint_.+?_name', 'fixVersions_.+?_name']
    
    @property
    def query(self):
        '''Return the user-provided JQL query'''
        return self._jql

    
