#!bin/python

'''
cycle_times.py

Author: Andrew Hamlin

Description: A command line tool to export changelog history using Jira Cloud REST API. The
goal is to correlate the estimated cycle time with the estimated story points assigned.

'''


from functools import partial
import sys
import argparse
import getpass
import dateutil.parser
import datetime

# project imports
from log import Log
from jira import Jira
    
            
def process_story_cycle_times (story):
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

    start_time = datetime.datetime(datetime.MINYEAR, 1, 1)
    end_time = datetime.datetime(datetime.MINYEAR, 1, 1)
    if cycle_times:
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
    parser.add_argument('-p', '--project', metavar='Project', action='append', help='Project name')
    
    parser.add_argument('-o', '--outfile', metavar='Output', nargs='?', type=argparse.FileType('w'), help='Output filename, default stdout', default=sys.stdout)
    parser.add_argument('-b', '--base_url', metavar='Base URL', help='Jira Cloud Base URL', default='sailpoint.atlassian.net')
    parser.add_argument('-u', '--user', metavar='User', help='Username', required=True)
    parser.add_argument('-w', '--password', metavar='Pwd', help='Password (insecure)', default=None)
    parser.add_argument('-d', action='count', help='Debug levels')
    
    args = parser.parse_args()

    if args.d:
        Log.global_DEBUG = args.d

    # we will be updating these later
    password = args.password
    outfile  = args.outfile
        
    ## Debugging
    Log.debug('Base URL: ', args.base_url)
    Log.debug('Project: ',  args.project)
    Log.debug('Issues: ',  args.issues)
    Log.debug('User: ',     args.user)
    Log.debug('Output: ',   args.outfile)
    Log.verbose('Debug flag: ', Log.global_DEBUG)
    ##

    if args.project is None and len(args.issues) == 0:
        raise Exception('specify a project or list of issues')
    
    # grab password from stdin
    if not args.password:
        password = getpass.getpass()
        
    jira = Jira(args.base_url, username=args.user, password=password)

    if args.project is not None:
        projects = ', '.join(args.project)
        statuses = ', '.join(['Done', 'Accepted'])
        jql_query = 'project in ({}) AND issuetype = Story AND status in ({})'.format(projects, statuses)

        get_issues = partial(jira.get_project_issues, jql_query)
    else:
        get_issues = partial(jira.get_issues, args.issues)

    if outfile.closed:
        outfile = open(args.outfile, 'w')

    Log.info('Retrieving issues...')

    # REFACTOR - either: provide operations, such as -cycletime, or create multiple __main__ scripts for each operation

    outfile.write('issue,storypoints,start,end\n')
    try:

        for story in get_issues():
            print(story.get('fields'))
            outfile.write(','.join(map(str, process_story_cycle_times(story))))
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
