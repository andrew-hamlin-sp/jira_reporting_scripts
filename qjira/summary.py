'''Summarize the backlog'''

from .data import calculate_rows

class Summary:

    def __init__(self):
        self._fieldnames = ['project_key','fixVersions_0_name','issuetype_name','issue_key','summary','epic_issuekey','design_doc_link','testplan_doc_link','sprint_0_name','sprint_0_startDate','story_points']
        self._query = 'issuetype = Story'

    @property
    def header(self):
        return self._fieldnames

    @property
    def query(self):
        return self._query

    def process(self, issues):
        results = [row for iss in issues for row in calculate_rows(iss)]
        return results
