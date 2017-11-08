#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
main.py
Author: Andrew Hamlin
Description: script to execute commands against jira
'''
import sys
import io
import argparse
import locale

from requests.exceptions import HTTPError

from .velocity import VelocityCommand
from .cycletime import CycleTimeCommand
from .summary import SummaryCommand
from .techdebt import TechDebtCommand
from .backlog import BacklogCommand
from .jql import JQLCommand
from .log import Log
from . import unicode_csv_writer
from . import credential_store as creds

PY3 = sys.version_info > (3,)

def _print(msg):
    sys.stderr.write(msg)
    sys.stderr.flush()

def _progress(start, total):
    msg = '\rRetrieving {} of {}...'.format(start, total)
    if start >= total:
        msg = ' ' * len(msg)
        _print('\r' + msg)
        msg += '\rRetrieved {} issues\n'.format(start, total)
    _print(msg)    

def _open(filepath, encoding):
    '''Open the file with given encoding.

    If the filepath is the default sys.stdout, just return it.
    '''
    if not filepath:
        return sys.stdout
    elif PY3:
        return io.open(filepath, 'wt',
                       encoding=encoding,
                       newline='')
    else:
        return io.open(filepath, 'wb')
    
def create_parser():


    parser = argparse.ArgumentParser(prog='qjira',
                                     description='Export data from Jira to CSV format')
    
    parser.add_argument('-o', '--outfile',
                               metavar='FILENAME',
                               nargs='?',
                               default=None,
                               help='Output file (.csv) [default: stdout]')

    parser.add_argument('--no-progress',
                               action='store_true',
                               dest='suppress_progress',
                               help='Hide data download progress')       

    parser.add_argument('-b', '--base',
                               dest='base_url',
                               metavar='URL',
                               help='Jira Cloud base URL [default: sailpoint.atlassian.net]',
                               default='sailpoint.atlassian.net')

    parser.add_argument('-u', '--user',
                               metavar='USER',
                               help='Username, if blank will use logged on user',
                               default=None)

    parser.add_argument('-w', '--password',
                               metavar='PWD',
                               help='Password (insecure), if blank will prommpt',
                               default=None)
    
    parser.add_argument('--encoding',
                               metavar='ENC',
                               default='ASCII',
                               help='Specify an output encoding. In Python 2.x, only default ASCII is supported.')
    parser.add_argument('--delimiter',
                               metavar='CHAR',
                               default=',',
                               help='Specify a CSV delimiter [default: comma].\nFor bash support escape the character with $, such as $\'\\t\'')

    parser.add_argument('-d',
                        dest='debugLevel',
                        action='count',
                        help='Debug level')

    parser.set_defaults(func=None)

    # sub-commands: velocity, cycletimes, summary, techdebt
    subparsers = parser.add_subparsers(title='Available commands',
                                       dest='subparser_name',
                                       help='Available commands to process data')

    parser_common = argparse.ArgumentParser(add_help=False)
    
    parser_common.add_argument('-A', '--all-fields',
                               action='store_true',
                               help='Extract all "navigable" fields in Jira, [fields=*navigable]')

    parser_command_options = argparse.ArgumentParser(add_help=False,
                                                     parents=[parser_common])
        
    parser_command_options.add_argument('-f', '--fix-version',
                               dest='fixversion',
                               metavar='VERSION',
                               action='append',
                               help='Restrict search to fixVersion(s)')

    parser_command_options.add_argument('project',
                                        nargs='+',
                                        metavar='project',
                                        help='Project name')

    
    parser_cycletime = subparsers.add_parser('cycletime',
                                             parents=[parser_command_options],
                                             help='Produce cycletime data')
    parser_cycletime.set_defaults(func=CycleTimeCommand)

    parser_velocity = subparsers.add_parser('velocity',
                                            parents=[parser_command_options],
                                            help='Produce velocity data')
    parser_velocity.add_argument('--include-bugs', '-B',
                                 action='store_true',
                                 help='Include bugs in velocity calculation')
    parser_velocity.add_argument('--forecast', '-F',
                                action='store_true',
                                help='Include future sprints in velocity calculation')
    parser_velocity.add_argument('--raw', '-R',
                                 action='store_true',
                                 help='Output all rows instead of summary by sprint name.')
    parser_velocity.set_defaults(func=VelocityCommand)

    parser_summary = subparsers.add_parser('summary',
                                           parents=[parser_command_options],
                                           help='Produce summary report')
    parser_summary.add_argument('--mark-new', '-N',
                                action='store_true',
                                dest='mark_if_new',
                                help='Mark docs linked within past 2 weeks')
    parser_summary.set_defaults(func=SummaryCommand)

    parser_techdebt = subparsers.add_parser('debt',
                                            parents=[parser_command_options],
                                            help='Produce tech debt report')
    parser_techdebt.set_defaults(func=TechDebtCommand)

    parser_backlog = subparsers.add_parser('backlog',
                                           parents=[parser_command_options],
                                           help='Query bug backlog by fixVersion')
    parser_backlog.set_defaults(func=BacklogCommand)
    



    parser_jql = subparsers.add_parser('jql',
                                       parents=[parser_common],
                                       help='Query using JQL')

    parser_jql.add_argument('jql',
                            help='JQL statement')

    parser_jql.add_argument('--add-field', '-f',
                            action='append',
                            metavar='NAME',
                            help='Add field(s) to Jira request')

    parser_jql.add_argument('--add-column', '-c',
                            action='append',
                            metavar='NAME',
                            help='Add column(s) to CSV output')
    
    parser_jql.set_defaults(func=JQLCommand)
                                       
    
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
                              'suppress_progress', 'user', 'password',
                              'delimiter', 'encoding']}

    # build up some additional keyword args for the commands
    if not my_args.suppress_progress:
        func_args.update({'progress_cb': _progress})

    # get/store user private Jira credentials from OS keyring
    username, password = creds.get_credentials(my_args.user,
                                               my_args.password)
    func_args.update({
        'username': username,
        'password': password
    })

    Log.debug('Args: {0}'.format(func_args))
    command = my_args.func(**func_args)
    try:
        with _open(my_args.outfile, my_args.encoding) as f:
            unicode_csv_writer.write(f, command, my_args.encoding,
                                     delimiter=my_args.delimiter)
    except HTTPError as err:
        if err.response.status_code == 401:
            creds.clear_credentials(username)
        raise err

if __name__ == "__main__":
    locale.setlocale(locale.LC_TIME, 'en_US')
    main(args=sys.argv[1:])

