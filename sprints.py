#!bin/python
'''
sprints.py

Author: Andrew Hamlin

Description: A command line tool to export data using Jira Cloud REST API. The goal
is to flatten exported data by iterations (sprint).
'''

from functools import partial
import sys
import argparse
import re
import getpass

# project imports
from log import Log
from jira import Jira

def sprint_info (sprint):
    '''Return object from string representation: 'com.atlassian.greenhopper.service.sprint.Sprint@be7f5f[id=82,rapidViewId=52,state=CLOSED,name=Chambers Sprint 9,goal=<null>,startDate=2016-04-25T10:44:22.273-05:00,endDate=2016-05-09T10:44:00.000-05:00,completeDate=2016-05-09T10:48:04.212-05:00,sequence=82]'
    '''
    m = re.search('\[(.+)\]', sprint)
    if m:
        return dict(e.split('=') for e in m.group(1).split(','))
    return None

def process_story_sprints (story):
    '''Extract tuple containing sprint, issuekey, and story points from Story'''
    issuekey = story['key']
    points = story['fields'].get('customfield_10109')

    sprints = story['fields'].get('customfield_10016')

    if sprints is None:
       yield ('', issuekey, points)
       return
       
    # Jira returns list of Sprints as an array of strings that are Java object
    infos = [sprint_info(sprint) for sprint in sprints]

    for info in infos:
        yield (info['name'], issuekey, points)

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
        jql_query = 'project in ({}) AND issuetype = Story'.format(projects)

        get_issues = partial(jira.get_project_issues, jql_query)
    else:
        get_issues = partial(jira.get_issues, args.issues)

    if outfile.closed:
        outfile = open(args.outfile, 'w')

    Log.info('Retrieving issues...')

    outfile.write('sprint,issue,storypoints\n')
    try:

        for story in get_issues():
            #print(story.get('fields'))
            for info in process_story_sprints(story):
            #outfile.write(','.join(map(str, process_story_sprints(story))))
                outfile.write(','.join(map(str, info)))
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
