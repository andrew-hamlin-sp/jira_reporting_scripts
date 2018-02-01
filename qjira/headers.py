'''Map of column headers to user-friendly names. 

No localization support.
'''

HEADER = {
    'issue_link': 'Issue',
    'summary': 'Summary',
    'assignee_displayName': 'Assignee',
    'design_doc_link': 'Design Doc',
    'testplan_doc_link': 'Test Plan',
    'story_points': 'Story Points',
    'status_name': 'Status',
    'epic_link': 'Epic',
    'project_key': 'Project',
    'project_name': 'Project Name',
    'fixVersions_name': 'Fix Version',
    'issuetype_name': 'Issue Type',
    'issue_key': 'Issue Key',
    'priority_name': 'Priority',
    'created': 'Created',
    'updated': 'Updated',
    'severity_value': 'Severity',
    'customer': 'Customer',
    'fixVersions_0_name': 'Fix Version',
    'status_InProgress': 'In Progress',
    'count_days': 'Days',
    'bug_points': 'Bug Points',
    'tech_debt': 'Tech Debt %',
    'sprint_name': 'Sprint',
    'sprint_startDate': 'Start Date',
    'sprint_endDate': 'End Date',
    'planned_points': 'Planned',
    'carried_points': 'Carried',
    'completed_points': 'Completed',
}

def get_column_header(key):
    '''Return the user-friendly name of column'''
    return HEADER.setdefault(key, key)

def get_column(key):
    '''Return tuple including column key and header'''
    return key, get_column_header(key)
