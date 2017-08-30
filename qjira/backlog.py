"""
Class encapsulating Backlog calculations. This will 
pivot the issues on fixVersion fields for sorting
between future unreleased versions and dev_backlog,
for example.
"""

from .command import Command
from .dataprocessor import DataProcessor
from .log import Log

class Backlog(Command):

    def __init__(self, *args, **kwargs):
        Command.__init__(self, args, kwargs, processor=DataProcessor(pivot='fixVersions'))

        self._fieldnames = ['project_key', 'fixVersions_name', 'issuetype_name', 'issue_key']
        self._query = 'issuetype = Bug AND resolution = Unresolved ORDER BY priority DESC'

    @property
    def header(self):
        return self._fieldnames

    @property
    def query(self):
        return self._query


    def post_process(self, rows):
        return rows
