#!python
'''
main.py
Author: Andrew Hamlin
Description: script to execute commands against jira
'''

import sys
import argparse
import getpass
import csv

from .velocity import Velocity
from .cycletime import CycleTime
from .jira import Jira
from .log import Log

OLDSTRING = ''

def _report ( msg ):
    global OLDSTRING
    sys.stderr.write('\r' + (' ' * len(OLDSTRING)))
    sys.stderr.write('\r' + msg)
    OLDSTRING = msg


def main():
    # process command line arguments

    parser_common = argparse.ArgumentParser(add_help=False)
    
    parser_common.add_argument('-p', '--project',
                        metavar='project',
                        action='append',
                        required=True,
                        help='Project name')
    parser_common.add_argument('-F', '--fix-version',
                        dest='fixversion',
                        metavar='fixVersion',
                        action='append',
                        help='Restrict search to fixVersion(s)')
    parser_common.add_argument('-o', '--outfile',
                        metavar='file',
                        type=argparse.FileType('w'),
                        help='Output file (.csv) [default: stdout]',
                        default=sys.stdout)
    parser_common.add_argument('--show-progress',
                        action='store_true',
                        help='Display JIRA data download progress')       
    parser_common.add_argument('-b', '--base',
                        metavar='url',
                        help='Jira Cloud base URL [default: sailpoint.atlassian.net]',
                        default='sailpoint.atlassian.net')
    parser_common.add_argument('-u', '--user',
                        metavar='user',
                        help='Username [default: %s]' % getpass.getuser(),
                        default=None)
    parser_common.add_argument('-w', '--password',
                        metavar='pwd',
                        help='Password (insecure), if blank will prommpt',
                        default=None)
    parser_common.add_argument('-d',
                        action='count',
                        help='Debug level')

    parser = argparse.ArgumentParser(description='Export data from Jira to CSV format')

    # sub-commands: velocity, cycletimes
    # TODO: add backlog/loading by sprint

    subparsers = parser.add_subparsers(dest='subparser_name', help='Available commands to process data')

    parser_cycletime = subparsers.add_parser('c',
                                             parents=[parser_common],
                                             help='Produce [c]ycletime data')
    parser_cycletime.set_defaults(func=CycleTime)

    parser_velocity = subparsers.add_parser('v',
                                            parents=[parser_common],
                                            help='Produce [v]elocity data')
    parser_velocity.add_argument('--exclude-carryover',
                                 action='store_true',
                                 help='Exclude points carried-over to future sprints')
    parser_velocity.set_defaults(func=Velocity)

    args = parser.parse_args()
    
    if args.d:
        Log.debugLevel = args.d

    if not args.user:
        args.user = getpass.getuser()
        
    if not args.password:
        args.password = getpass.getpass('Enter password for {}'.format(args.user))
    
    # TODO: store credentials in a user protected file and pass in as 'auth=XXX'

    progress = _report if args.show_progress else None
    
    jira = Jira(args.base, username=args.user, password=args.password, progress=progress)

    processor = args.func(project=args.project, fixversion=args.fixversion)

    outfile = args.outfile

    issues = jira.get_project_issues(processor.query)
    
    Log.debug('Process {} issues'.format(len(issues)))

    fieldnames = processor.header # TODO convert to array
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for entry in processor.process(issues):
        writer.writerow(entry)

    outfile.close()


if __name__ == "__main__":
    main()

