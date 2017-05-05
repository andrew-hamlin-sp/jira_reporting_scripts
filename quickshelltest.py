
import sys
import json
import requests
import csv
import re
import dateutil.parser

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

USER='andrew.hamlin'
PASS='eU=ETI-|Sc8mz8|V'


ISSUE_ENDPOINT='https://{}/rest/api/2/issue/{}?{}'

    
HEADERS = {'content-type': 'application/json'}

# expands the changelog of each issue and hides all but essential fields
# customfield 10109 is the 'story points' field
# customfield 10016 is the 'iteration' or 'sprint' field, an array
QUERY_STRING_DICT = {
  'expand': 'changelog',
  'fields': '-*navigable,project,issuetype,customfield_10109,customfield_10016'
}


search_args = QUERY_STRING_DICT.copy()

# issuekey
key = sys.argv[1]

if not key:
    raise ValueError

#search_args.update({
#  'jql':'issuekey = {}'.format(key)
#})

query_string = urlencode(search_args)

base_url = 'sailpoint.atlassian.net'
url = ISSUE_ENDPOINT.format(base_url, key, query_string)

r = requests.get(url, auth=(USER, PASS), headers=HEADERS)
r.raise_for_status()

data = r.json()

with open('debug.json', 'w') as f:
    json.dump(data, f)
  
#total = json['total']
#issues = json['issues']
#count = len(issues)

def generate_name(*args):
    return '_'.join([str(a) for a in args])

#print(json)
def _extract_sprint(sprint):
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


def transform_dict(name, value):
    yield [(generate_name(name, k1),v1) for k1, v1 in value.items()]

def transform_list(name, value):
    for idx,item in enumerate(value):
        yield [(generate_name(name, idx, k1),v1) for k1, v1 in item.items()]
    return

# flatten the dictionary object `json`
def mapper(name, value):
    value_type = type(value)

    print('>> name {} value_type {}'.format(name, value_type))

    if value_type is dict:
        for subitem in transform_dict(name, value):
            yield subitem
    elif value_type is list:
        for subitem in transform_list(name, value):
            yield subitem
    else:
        yield { name: value }

    return


def process_issue(data, pivot=None):

    # fields include issuetype, project, story points (customfield_10109) and sprints (customfield_10016)

  
    issue = dict(issuekey=data['key'])
  
    # -- begin pre-process
    # update dictionary to reflect known names for custom fields
    if data['fields'].get('customfield_10016'):
        data['fields']['sprint'] = [sprint for sprint in map(_extract_sprint, data['fields']['customfield_10016'])]
        del data['fields']['customfield_10016']

    if data['fields'].get('customfield_10109'):
        data['fields']['story_points'] = data['fields']['customfield_10109']
        del data['fields']['customfield_10109']
    # -- end pre-process

    # -- begin process
    # process all the fields
    for k,v in data['fields'].items():
        if not v:
            continue

        if pivot == k: # -- skip field used for pivot
            continue

        print('> field {} is {}'.format(k, v))
    
        for field in mapper(k, v):
            issue.update(field)
    # -- end process

    
    # changelog histories
    # TODO
    histories = [dict(i.items(), created=h['created'])
                 for h in data['changelog']['histories']
                 for i in h['items'] if i['field'] == 'status']

    #  return sorted(history, key=lambda x: x['created']) if history else None
    # create csv entries status_InProgress: {created}, status_Done: {created}

    for history in histories:
        #status_name = history['items']
        print('> history {}'.format(history))
        status_name = '_'.join([history['field'], history['toString'].replace(' ', '')])
        status_value = dateutil.parser.parse(history['created']).date()
        print('> update {}={}'.format(status_name, status_value))
        issue.update({status_name:status_value})
    
    # -- begin pivot
    if pivot and data['fields'].get(pivot):
        for src_idx, src_item in enumerate(data['fields'][pivot]):
            print ('> src_idx {} is {}'.format(src_idx, src_item))
            pivot_item = {}
            for field in mapper(pivot, src_item):
                pivot_item.update(field)
        
            pivot_item.update(issue)
            print ('> pivot_item {}'.format(pivot_item))
            yield pivot_item
        return
    # -- end pivot

    yield issue
      

doPivot =  'sprint' # | None

results = [result for result in process_issue(data, pivot=doPivot)]

if not results:
    sys.exit(1)

print('> dict keys: {}'.format(','.join([str(k) for k in results[0].keys()])))

# basic fields
# TODO pivot on sprints for velocity
# TODO calculate changelog histories ranges for cycletime
fieldnames=[
    'project_key',
    'issuekey',
    'issuetype_name',
    'sprint_0_name', # -- flat
    'sprint_name',    # -- velocity, pivot 'sprint'
    'sprint_state',    # -- velocity, pivot 'sprint'
    'story_points',
    'status_Open',
    'status_InProgress',
    'status_Done'
]
  
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction='ignore')
writer.writeheader()
for result in results:
    writer.writerow(result)


#from qjira.issue import Issue

#with open('doc/test.json') as f:
#  j1 = json.load(f)

#with open('doc/test_bug.json') as f:
#  j2 = json.load(f)

#print('loading sample Story test.json') 
#Issue(j1)

#print('loading sample Bug test_bug.json')
#Issue(j2)

