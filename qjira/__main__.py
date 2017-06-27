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

import locale

from .velocity import Velocity
from .cycletime import CycleTime
from .summary import Summary
from .jira import Jira
from .log import Log
from .container import Container

def _progress (start, total):
    msg = '\rRetrieving {} of {}...'.format(start, total)
    if start >= total:
        msg = ' ' * len(msg)
        sys.stderr.write('\r' + msg)
        sys.stderr.flush()
        msg += '\rRetrieved {} issues\n'.format(start, total)
    sys.stderr.write(msg)
    sys.stderr.flush()

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
                        nargs='?',
                        help='Output file (.csv) [default: stdout]')
    parser_common.add_argument('--no-progress',
                        action='store_true',
                        dest='suppress_progress',
                        help='Hide data download progress')       
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
    parser_common.add_argument('-1', '--one-shot',
                        action='store_true',
                        help='Exit after 1 HTTP request (for debug purpose only)')
    parser_common.add_argument('-A', '--all-fields',
                        action='store_true',
                        help='Extract all available fields')

    parser = argparse.ArgumentParser(description='Export data from Jira to CSV format')

    # sub-commands: velocity, cycletimes
    # TODO: add backlog/loading by sprint, add summary including description, design & test docs

    subparsers = parser.add_subparsers(dest='subparser_name', help='Available commands to process data')

    parser_cycletime = subparsers.add_parser('c',
                                             parents=[parser_common],
                                             help='Produce [c]ycletime data')
    parser_cycletime.set_defaults(func=CycleTime)

    parser_velocity = subparsers.add_parser('v',
                                            parents=[parser_common],
                                            help='Produce [v]elocity data')
    parser_velocity.set_defaults(func=Velocity)

    parser_summary = subparsers.add_parser('s',
                                           parents=[parser_common],
                                           help='Produce [s]ummary report')
    parser_summary.set_defaults(func=Summary)
    
    args = parser.parse_args()
    
    if args.d:
        Log.debugLevel = args.d

    if not args.user:
        args.user = getpass.getuser()
        
    if not args.password:
        args.password = getpass.getpass('Enter password for {}: '.format(args.user))
    
    # TODO: store credentials in a user protected file and pass in as 'auth=XXX'

    if args.suppress_progress:
        func_progress = None
    else:
        func_progress=_progress

    svc = Container()
    svc['jira'] = Jira(args.base, username=args.user, password=args.password, one_shot=args.one_shot, all_fields=args.all_fields, progress=func_progress)
    
    processor = args.func()

    try:
        outfile = open(args.outfile, 'w', newline='') if args.outfile else sys.stdout
    except TypeError:
        outfile = open(args.outfile, 'wb') if args.outfile else sys.stdout
        
    query = []
    if args.fixversion:
        query.append('fixVersion in ({})'.format(','.join(args.fixversion)))
    if args.project:
        query.append('project in ({})'.format(','.join(args.project)))
    if processor.query:
        query.append(processor.query)

    query_string = ' AND '.join(query)

    issues = svc['jira'].get_project_issues(query_string)
        
    fieldnames = processor.header # TODO convert to array
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()

    for entry in processor.process(issues):
        writer.writerow(entry)

    outfile.close()


if __name__ == "__main__":

    locale.setlocale(locale.LC_TIME, 'en_US')
    
    main()

