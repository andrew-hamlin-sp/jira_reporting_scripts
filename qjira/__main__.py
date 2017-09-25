#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
main.py
Author: Andrew Hamlin
Description: script to execute commands against jira
'''

import sys
import argparse

import locale
from requests.exceptions import HTTPError

from .velocity import VelocityCommand
from .cycletime import CycleTimeCommand
from .summary import SummaryCommand
from .techdebt import TechDebtCommand
from .backlog import BacklogCommand
from .log import Log
from . import unicode_csv_writer
from . import credential_store as creds

def _progress(start, total):
    msg = '\rRetrieving {} of {}...'.format(start, total)
    if start >= total:
        msg = ' ' * len(msg)
        sys.stderr.write('\r' + msg)
        sys.stderr.flush()
        msg += '\rRetrieved {} issues\n'.format(start, total)
    sys.stderr.write(msg)
    sys.stderr.flush()

def create_parser():
    parser_common = argparse.ArgumentParser(add_help=False)
    parser_common.add_argument('project',
                               nargs='+',
                               metavar='project',
                               help='Project name')
    parser_common.add_argument('-f', '-F', '--fix-version',
                               dest='fixversion',
                               metavar='fixVersion',
                               action='append',
                               help='Restrict search to fixVersion(s)')
    parser_common.add_argument('-o', '--outfile',
                               metavar='file',
                               nargs='?',
                               default=sys.stdout,
                               help='Output file (.csv) [default: stdout]')
    parser_common.add_argument('--no-progress',
                               action='store_true',
                               dest='suppress_progress',
                               help='Hide data download progress')       
    parser_common.add_argument('-b', '--base',
                               dest='base_url',
                               metavar='url',
                               help='Jira Cloud base URL [default: sailpoint.atlassian.net]',
                               default='sailpoint.atlassian.net')
    parser_common.add_argument('-u', '--user',
                               metavar='user',
                               help='Username, if blank will use logged on user',
                               default=None)
    parser_common.add_argument('-w', '--password',
                               metavar='pwd',
                               help='Password (insecure), if blank will prommpt',
                               default=None)
#    parser_common.add_argument('-1', '--one-shot',
#                        action='store_true',
#                        help='Exit after 1 HTTP request (for debug purpose only)')
    parser_common.add_argument('-A', '--all-fields',
                               action='store_true',
                               help='Extract all available fields')

    parser = argparse.ArgumentParser(prog='qjira',
                                     description='Export data from Jira to CSV format')
    parser.add_argument('-d',
                        dest='debugLevel',
                        action='count',
                        help='Debug level')
    parser.set_defaults(func=None)

    # sub-commands: velocity, cycletimes, summary, techdebt
    subparsers = parser.add_subparsers(title='Available commands',
                                       dest='subparser_name',
                                       help='Available commands to process data')
    
    parser_cycletime = subparsers.add_parser('cycletime',
                                             parents=[parser_common],
                                             help='Produce cycletime data')
    parser_cycletime.set_defaults(func=CycleTimeCommand)

    parser_velocity = subparsers.add_parser('velocity',
                                            parents=[parser_common],
                                            help='Produce velocity data')
    parser_velocity.set_defaults(func=VelocityCommand)
    parser_velocity.add_argument('--include-bugs', '-B',
                                 action='store_true',
                                 help='Include bugs in velocity calculation')

    parser_summary = subparsers.add_parser('summary',
                                           parents=[parser_common],
                                           help='Produce summary report')
    parser_summary.set_defaults(func=SummaryCommand)

    parser_techdebt = subparsers.add_parser('debt',
                                            parents=[parser_common],
                                            help='Produce tech debt report')
    parser_techdebt.set_defaults(func=TechDebtCommand)

    parser_backlog = subparsers.add_parser('backlog',
                                           parents=[parser_common],
                                           help='Query bug backlog by fixVersion')
    parser_backlog.set_defaults(func=BacklogCommand)
    
    return parser

def main(args=None):
    
    parser = create_parser()
    my_args = parser.parse_args(args)

    if not my_args.func:
         parser.print_usage()
         raise SystemExit()

    if my_args.debugLevel:
        Log.debugLevel = my_args.debugLevel
    
    # filter out arguments commands do not need to understand
    func_args = {k:v for k,v in vars(my_args).items()
                 if k not in ['func', 'subparser_name', 'outfile', 'debugLevel',
                              'suppress_progress', 'user', 'password']}

    # build up some additional keyword args for the commands
    if not my_args.suppress_progress:
        func_args.update({'progress_cb': _progress})

    username, password = creds.get_credentials(my_args.user,
                                               my_args.password)
    func_args.update({
        'username': username,
        'password': password
    })

    command = my_args.func(**func_args)
    try:
        unicode_csv_writer.write(my_args.outfile, command)
    except HTTPError as err:
        creds.clear_credentials(username)
        raise err

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, 'en_US')
    main(args=sys.argv[1:])

