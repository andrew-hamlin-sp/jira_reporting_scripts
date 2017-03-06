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

from __future__ import print_function
from functools import partial
import sys
import argparse
import requests
import getpass

import json

from urllib.parse import urlencode
import dateutil.parser

# globals
global_DEBUG = 0

# Note: expanding the changelog for the story does not give us the sub-task history
# which is what I was interested in researching. Need to loop through issues returned
# from a filter (query), find all sub-tasks, then retrieve expanded changelog of all
# those items to produce historical data necessary

class Log:
    '''Simple logger'''

    def eprint (*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
        
    eprint = eprint

    def error (*msg):
        '''Log as an error'''
        Log.eprint('[ERROR]', *msg)
        
    def info (*msg):
        '''Log message when debug >= 0'''
        if global_DEBUG < 0:
            return
        Log.eprint('[INFO]', *msg)

    info = staticmethod(info)

    def debug (*msg):
        '''Log message when debug >= 1'''
        if global_DEBUG < 1:
            return
        Log.eprint('[DEBUG]', *msg)

    debug = staticmethod(debug)
        
    def verbose (*msg):
        '''Log message when debug >= 2'''
        if global_DEBUG < 2:
            return
        Log.eprint('[VERBOSE]', *msg)

    verbose = staticmethod(verbose)

            
class Jira:

    # constants
    ISSUE_ENDPOINT='https://{}/rest/api/2/issue/{}?{}'

    ISSUE_SEARCH_ENDPOINT='https://{}/rest/api/2/search?{}'
    
    HEADERS = {'content-type': 'application/json'}
            
    def __init__ (self, baseUrl, **kwargs):
        ''' Construct new Jira client '''
        self.baseUrl = baseUrl
        for k in ('username', 'password'):
            setattr(self, k, kwargs.get(k))

    def get_issues (self, issues):
        '''Generator returning json of all issues'''

        query_string = urlencode({
            'expand': 'changelog',
            'fields': '-*navigable,customfield_10109'
        })
        
        for n in issues:
            url = Jira.ISSUE_ENDPOINT.format(self.baseUrl, n, query_string)
            Log.debug(url)

            # retrieve parent
            r = requests.get(url, auth=(self.username, self.password), headers=Jira.HEADERS)
            Log.debug(r.status_code)
            
            # TODO assert issuetype is story
            r.raise_for_status()

            json = r.json()

            yield json

    def get_project_issues (self, projectname):

        query_string = urlencode({
            'jql': 'project = {} AND issuetype = Story AND status in (Done, Accepted)'.format(projectname),
            'expand': 'changelog',
            'fields': '-*navigable,customfield_10109'
        })

        url = Jira.ISSUE_SEARCH_ENDPOINT.format(self.baseUrl, query_string)
        Log.debug(url)

        
        r = requests.get(url, auth=(self.username, self.password), headers=Jira.HEADERS)

        Log.debug(r.status_code)
        r.raise_for_status()

        json = r.json()

        # return and process each issue
        return json['issues']

    
class CryptoKeys:
    '''Steps to encrypt/decrypt using cryptography package

    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes


    with open("/Users/andrew.hamlin/.ssh/id_rsa.pub", "rb") as key_file:
        pub_key = serialization.load_ssh_public_key(key_file.read(), default_backend())
    with open("/Users/andrew.hamlin/.ssh/id_rsa", "rb") as key_file:   
        pri_key = serialization.load_pem_private_key(key_file.read(), password=b"PASSWORDHERE", backend=default_backend())

    cipher = pub_key.encrypt(b"hello", padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
    pri_key.decrypt(cipher, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None))
    '''
    pass

            
def process_story (story):
    '''Extract tuple containing issuekey, story points, and cycle time from Story'''
    
    issuekey = story['key']
    points = story['fields'].get('customfield_10109')
                  
    cycle_times = [dateutil.parser.parse(entry['created'])
                   for entry in story['changelog'].get('histories')
                   if entry['items'][0].get('field') == 'status'
                   and (
                       entry['items'][0].get('to') == '3'
                       or  entry['items'][0].get('to') == '10001'
                   )]
    # sort by created date so we can use find first In Progress and last Done status
    sorted_times = sorted(cycle_times)
    #print(sorted_times)
    
    start_time = sorted_times[0]
    end_time = sorted_times[-1]
#    delta = end_time - start_time
            
    return (issuekey, points, start_time.date(), end_time.date())

            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export detailed history of a project to CSV file')

    # query for specific items or by an entire project
    parser.add_argument('issues', metavar='Issue', nargs='*', help='List of issues to retrieve')
    parser.add_argument('-p', '--project', metavar='Project', help='Project name')
    
    parser.add_argument('-o', '--outfile', metavar='Output', nargs='?', type=argparse.FileType('w'), help='Output filename, default stdout', default=sys.stdout)
    parser.add_argument('-b', '--base_url', metavar='Base URL', help='Jira Cloud Base URL', default='sailpoint.atlassian.net')
    parser.add_argument('-u', '--user', metavar='User', help='Username', required=True)
    parser.add_argument('-w', '--password', metavar='Pwd', help='Password (insecure)', default=None)
    parser.add_argument('-d', action='count', help='Debug levels')
    
    args = parser.parse_args()

    # Setup variables
    base_url = args.base_url
    project = args.project
    username=args.user
    password=args.password

    outfile=args.outfile

    if args.d:
        global_DEBUG = args.d
    
    ## Debugging
    Log.debug('Base URL: ', base_url)
    Log.debug('Project: ', project)
    Log.debug('User: ', username)
    Log.debug('Output: ',outfile)
    Log.verbose('Debug flag: ', global_DEBUG)
    ##

    if project is None and args.issues is None:
        raise Exception('specify a project or list of issues')

    if project is None and args.issues is None:
        raise Exception('missing issues')
    
    # grab password from stdin
    if not password:
        password = getpass.getpass()
        
    jira = Jira(base_url, username=username, password=password)

    if project is not None:
        get_issues = partial(jira.get_project_issues, project)
    else:
        get_issues = partial(jira.get_issues, args.issues)

    if outfile.closed:
        outfile = open(args.outfile, 'w')

    Log.info('Retrieving issues...')

    outfile.write('issue,storypoints,start,end\n')
    try:

        for story in get_issues():
            outfile.write(','.join(map(str, process_story(story))))
            outfile.write('\n')
    except Exception:
        Log.error('Unexpected error:', sys.exc_info()[0])
        raise

#    print (results)
#    outfile.write(json.dumps(results, indent=4, separators=(',',':')))

    if not outfile.closed:
        outfile.close()

    Log.info('Done')
        
    exit(0)
