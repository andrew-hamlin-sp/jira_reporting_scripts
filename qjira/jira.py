'''Executes simple queries of Jira Cloud REST API'''

import requests

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .log import Log
from .dataprocessor import extract_sprint, create_history

CUSTOM_FIELD_MAP = {
    'customfield_10016': 'sprint',
    'customfield_10017': 'epic_issue_key',
    'customfield_10109': 'story_points',
    'customfield_11101': 'design_doc_link',
    'customfield_14300': 'testplan_doc_link',
    'customfield_10112': 'severity',
    'customfield_10400': 'customer',
}

ISSUE_ENDPOINT='https://{}/rest/api/2/issue/{}'

ISSUE_SEARCH_ENDPOINT='https://{}/rest/api/2/search?{}'

ISSUE_BROWSE='https://{}/browse/{}'
    
HEADERS = {'content-type': 'application/json'}

DEFAULT_FIELDS = [
    '-*navigable',
    'project',
    'issuetype',
    'status',
    'summary',
    'assignee',
    'fixVersions',
    'customfield_10016',
    'customfield_10017',
    'customfield_10109'
]

DEFAULT_EXPANDS = [
    'changelog'
]

def _get_json(url, username=None, password=None, headers=HEADERS):
    r = requests.get(url, auth=(username, password), headers=headers)
    Log.debug(r.status_code)
    r.raise_for_status()        
    return r.json()

def _as_data(issue, reverse_sprints=False):
    data = {
        'issue_key':issue['key']
    }
    #copy in fields, replacing custom fields with mapped names
    data.update({CUSTOM_FIELD_MAP.get(k, k):v for k, v in issue['fields'].items()})
    #copy in sprints
    if issue['fields'].get('customfield_10016'):
        sprints_encoded = issue['fields']['customfield_10016']
        if sprints_encoded:
            data['sprint'] = [
                sprint for sprint in sorted(
                    map(extract_sprint, sprints_encoded),
                    key=lambda x: x['startDate'], reverse=reverse_sprints)
            ]
            #print('> as_data sprints sorted: {0}'.format(data['sprint']))
        
    #copy in changelog
    if issue.get('changelog'):
        histories = sorted(issue['changelog']['histories'], key=lambda x: x['created'])
        change_history = dict([create_history(dict(item, created=h['created']))
                               for h in histories for item in h['items'] if 'fieldId' in item])
        data.update(change_history)
        
    return data

def default_fields():
    '''Return fields to retrieve from Jira'''
    return DEFAULT_FIELDS[:]

def get_browse_url(baseUrl, issuekey):
    if not issuekey:
        raise ValueError
    return ISSUE_BROWSE.format(baseUrl, issuekey)

def get_issue(baseUrl, issuekey,username=None, password=None):
    # this does not pass in the query string
    url = ISSUE_ENDPOINT.format(baseUrl, issuekey)
    Log.debug('url = ' + url)
    return _as_data(_get_json(url, username=username, password=password))

def all_issues(baseUrl, jql,
               username=None,
               password=None,
               progress_cb=None,
               reverse_sprints=False,
               fields=DEFAULT_FIELDS,
               expands=DEFAULT_EXPANDS):
    '''Generator yielding a partially normalized structure from JSON'''
    Log.debug('all_issues')
    search_args = {
        'expand': ','.join(expands),
        'fields': ','.join(fields),
        'jql': jql
    }
    Log.debug('jql: ' + search_args['jql'])

    startAt = 0
    maxResults = 50
    total = maxResults
        
    while startAt < total:
        search_args.update({
            'startAt':startAt,
            'maxResults':maxResults
        })
        query_string = urlencode(search_args)
        url = ISSUE_SEARCH_ENDPOINT.format(baseUrl, query_string)
        Log.debug('url = ' + url)
        if progress_cb:
            progress_cb(startAt, total)
        payload = _get_json(url, username=username, password=password)
        #print('> payload {0}'.format(type(payload)))
        total = payload['total']
        issues = payload['issues']
        count = len(issues)
        startAt += count
        for issue in issues:
            yield _as_data(issue, reverse_sprints=reverse_sprints)

    if progress_cb:
        progress_cb(startAt, total)
