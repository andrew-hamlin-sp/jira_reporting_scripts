#!python
'''
main.py
Author: Andrew Hamlin
Description: script to execute commands against jira
'''

import sys
import argparse
import getpass

from log import Log
from jira import Jira
from cycle_times import CycleTime
from sprints import Velocity
    

if __name__ == "__main__":

    # process command line arguments

    parser_common = argparse.ArgumentParser(add_help=False)
    
    parser_common.add_argument('-p', '--project',
                        metavar='project',
                        action='append',
                        required=True,
                        help='Project name')
    parser_common.add_argument('-o', '--outfile',
                        metavar='file',
                        type=argparse.FileType('w'),
                        help='Output file (.csv) [default: stdout]',
                        default=sys.stdout)
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

    # sub-commands: cycletimes, backlog/loading by sprint

    subparsers = parser.add_subparsers(help='Available commands to process data')

    parser_cycletime = subparsers.add_parser('cycletime', aliases=['c'],
                                             parents=[parser_common],
                                             help='Produce cycletime data')
    parser_cycletime.set_defaults(func=CycleTime)

    parser_velocity = subparsers.add_parser('velocity', aliases=['v'],
                                            parents=[parser_common],
                                            help='Produce velocity data')
    parser_velocity.set_defaults(func=Velocity)

    args = parser.parse_args()
    
    if args.d:
        Log.debugLevel = args.d

    if not args.user:
        args.user = getpass.getuser()
        
    if not args.password:
        args.password = getpass.getpass()
        
    # TODO: store credentials in a user protected file and pass in as 'auth=XXX' 
    jira = Jira(args.base, username=args.user, password=args.password)

    processor = args.func(args, jira)

    outfile = args.outfile
    
    # write output
    if outfile.closed:
        Log.info('Opening outfile')
        outfile = open(args.outfile, 'w')

    outfile.write(processor.header + '\n')

    ## TODO Use the CSV module
    for entry in processor.process():
        outfile.write(','.join(map(str, entry)) + '\n')

    outfile.close()
                  
