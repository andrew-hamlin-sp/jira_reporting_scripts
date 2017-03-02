#!bin/python

'''
issueHistory.py

Author: Andrew Hamlin

Description: A command line tool to export changelog history using Jira Cloud REST API. The
goal is to correlate the estimated time with cycle time of the sub-tasks of an issue.

Workflow
 + Filter a project/sprint for stories
 + story.subtasks.foreach( retrieve subtask issue with ?expand=changelog parameter )
 + dump status changes in CSV format

'''

import sys
import argparse
import requests
import getpass

# globals
global_DEBUG = 0

# Note: expanding the changelog for the story does not give us the sub-task history
# which is what I was interested in researching. Need to loop through issues returned
# from a filter (query), find all sub-tasks, then retrieve expanded changelog of all
# those items to produce historical data necessary

class Log:

    def safe_print (*msg):
        print(' '.join(map(str,msg)))
    
    safe_printer = safe_print

    def error (*msg):
        '''Log as an error'''
        Log.safe_printer('[ERROR]', *msg)
        
    def info (*msg):
        '''Log message when debug >= 0'''
        if global_DEBUG < 0:
            return
        Log.safe_printer('[INFO]', *msg)

    info = staticmethod(info)

    def debug (*msg):
        '''Log message when debug >= 1'''
        if global_DEBUG < 1:
            return
        Log.safe_printer('[DEBUG]', *msg)

    debug = staticmethod(debug)
        
    def verbose (*msg):
        '''Log message when debug >= 2'''
        if global_DEBUG < 2:
            return
        Log.safe_printer('[VERBOSE]', *msg)

    verbose = staticmethod(verbose)

            
class Jira:

    # constants
    ISSUE_ENDPOINT='https://{}/rest/api/2/issue/{}?expand=changelog'
    HEADERS = {'content-type': 'application/json'}
            
    def __init__ (self, baseUrl, **kwargs):
        ''' Construct new Jira client '''
        self.baseUrl = baseUrl
        for k in ('username', 'password'):
            setattr(self, k, kwargs.get(k))

    def get_issues (self, issues):
        '''Generator returning json of all issues''' 
        for n in issues:
            url = Jira.ISSUE_ENDPOINT.format(self.baseUrl, n)
            Log.debug(url)

            # retrieve parent
            r = requests.get(url, auth=(self.username, self.password), headers=Jira.HEADERS)
            Log.debug(r.status_code)
            
            # TODO assert issuetype is story
            r.raise_for_status()

            json = r.json()

            yield json


def process (jira, issues):  
    outfile.write('\n'.join(map(process_story, jira.get_issues(issues))))


def process_story (story):
    '''Extract tuple containing issuekey, story points, and cycle time from Story'''
    
    issuekey = story['key']
    points = story['fields'].get('customfield_10109')
                  
    Log.info(issuekey, 'Story points:', points)

    # TODO perform a reduce on the elapsed time

    # changelog.histories [ filter: items.field='status' ]:
    # to 3, toString 'In Progress' = (created = start time), to 10001, toString 'Done' = (created = end time)

    cycle_times = filter(lambda entry: entry['items'][0].get('field') == 'status', story['changelog'].get('histories'))

    #Log.info(' '.join(map(str,cycle_times)))
    times = {}
    for st in cycle_times:
        k = st['items'][0].get('toString')
        v = st['created']
        if times.setdefault(k, v) != v:
            raise Exception('transition "{}" already exists'.format(k))

    Log.info('Collected times:', times)
    
    return ','.join(map(str, (issuekey, points)))

            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export detailed history of a project to CSV file')
    parser.add_argument('issues', metavar='ISSUE', type=str, nargs='+', help='Jira issuekey')
#    parser.add_argument('-p', '--project', metavar='Project', help='Project name')
    parser.add_argument('-o', '--outfile', metavar='Output', nargs='?', type=argparse.FileType('w'), help='Output filename, default stdout', default=sys.stdout)
    parser.add_argument('-b', '--base_url', metavar='Base URL', help='Jira Cloud Base URL', default='sailpoint.atlassian.net')
    parser.add_argument('-u', '--user', metavar='User', help='Username', required=True)
    parser.add_argument('-w', '--password', metavar='Pwd', help='Password (insecure)', default=None)
    parser.add_argument('-d', action='count', help='Debug levels')
    
    args = parser.parse_args()

    # Setup variables
    base_url = args.base_url
#    project = args.project
    username=args.user
    password=args.password

    outfile=args.outfile

    if args.d:
        global_DEBUG = args.d
    
    ## Debugging
    Log.debug('Base URL: ', base_url)
#    Log.debug('Project: ', project)
    Log.debug('User: ', username)
    Log.debug('Output: ',outfile)
    Log.verbose('Debug flag: ', global_DEBUG)
    ##
    Log.info("Retrieving issues...")
    
    # grab password from stdin
    if not password:
        password = getpass.getpass()

    jira = Jira(base_url, username=username, password=password)

    if outfile.closed:
        outfile = open(args.outfile, 'w')

    try:
        process(jira, args.issues)
    except Exception:
        Log.error('Unexpected error:', sys.exc_info()[0])
        raise

    if not outfile.closed:
        outfile.close()
        
    exit(0)
