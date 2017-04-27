'''Utility functions'''
import dateutil.parser
import re

def sprint_info (sprint):
    '''Return object from string representation: 'com.atlassian.greenhopper.service.sprint.Sprint@be7f5f[id=82,rapidViewId=52,state=CLOSED,name=Chambers Sprint 9,goal=<null>,startDate=2016-04-25T10:44:22.273-05:00,endDate=2016-05-09T10:44:00.000-05:00,completeDate=2016-05-09T10:48:04.212-05:00,sequence=82]'
        '''
    if not sprint:
        return dict()
    m = re.search('\[(.+)\]', sprint)
    if m:
        d = dict(e.split('=') for e in m.group(1).split(','))
        for n in ('startDate','endDate','completeDate'):
            try:
                d[n] = dateutil.parser.parse(d[n])
            except ValueError:
                d[n] = None
        return d
    raise ValueError

def get_issuetype (issue):
    if issue.get('fields') and issue['fields'].get('issuetype'):
        return issue['fields']['issuetype']['name']
    else:
        return None

def current_status (issue):
    if issue.get('fields') and issue['fields'].get('status'):
        return issue['fields']['status']['name']
    else:
        # Bugs record their state in the changelog history
        # JSON is already sorted with newest last, so just grab the last status
        status_field = [i['toString'] for h in issue['changelog']['histories'] for i in h['items'] if i['field'] == 'status']
        return status_field[-1] if status_field else None

def find_status_history (issue, status):
    history = [h for h in issue['changelog']['histories'] for i in h['items'] if i['field'] == 'status' and i['toString'] == status]
    return history[0] if history else None
