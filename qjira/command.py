""" Command base class for processing Jira issues"""

import abc
from functools import partial
import copy

from . import jira
from . import dataprocessor as dp
from .log import Log

def query_builder(name, items):
    return '{0} in ({1})'.format(name, ','.join(items))

class BaseCommand:

    __metaclass__ = abc.ABCMeta
    def __init__(self, base_url=None, project=[],
                 fixversion=[], all_fields=False,
                 *args, **kwargs):
        '''Initialize a command.
        
        Required Arguments:

        project - list of JIRA Project keys
        base_url -- JIRA Cloud instance, e.g. your-company.atlassian.net

        Optional Arguments:

        fixversion - list of FixVersion values
        '''
        if not project:
            raise TypeError('Missing keyword "project"')
        if not base_url:
            raise TypeError('Missing keyword "base_url"')

        self._projects = project
        self._base_url = base_url
        self._fixversions = fixversion
        self._all_fields = all_fields
        
        self.kwargs = kwargs
        # TODO handle all_fields
        self._http_request = self._configure_http_request()

    def _configure_http_request(self):
        '''Sub-classes can continue currying this function.'''
        #username = self.kwargs.pop('username')
        #password = self.kwargs.pop('password')
        #progress_cb = self.kwargs.pop('progress_cb')
        #all_fields = self.kwargs.pop('all_fields')
        return partial(jira.all_issues,
                       self._base_url,
                       fields=self._get_jira_fields(),
                       **self.kwargs)
                
    @abc.abstractproperty
    def header(self):
        '''Return the list of CSV column headers to print.'''
        raise NotImplementedError()

    @abc.abstractproperty
    def query(self):
        '''Return the JQL query for this command.'''
        raise NotImplementedError()

    def retrieve_fields(self, default_fields):
        '''Command may provide a set of Jira Fields. The provided list is
        a copy of the default that can be modified, appended or replaced.

        Argument:
        default_fields - list of default Jira fields
        '''
        return default_fields

    @property
    def count_fields(self):
        return []

    @property
    def datetime_fields(self):
        return ['lastViewed', 'created', 'updated']
    
    def _create_query_string(self):
        query = []
        if self._projects:
            query.append(query_builder('project', self._projects))
        if self._fixversions:
            query.append(query_builder('fixversion', self._fixversions))
        query.append(self.query)
        return ' AND '.join(query)

    def _get_jira_fields(self):
        if self._all_fields:
            return self.retrieve_fields(['*'])
        else:
            return self.retrieve_fields(jira.default_fields())

    def http_request(self):
        query_string = self._create_query_string()
        req = self._http_request(query_string)
        Log.debug('http_request: {0}'.format(req))
        return req

    def pre_process(self, generate_data):
        '''Override to construct a new data generator from the source generator'''
        Log.debug('pre_process: {0}'.format(generate_data))
        return generate_data

    def post_process(self, generate_rows):
        '''Override to construct a new row generator from the source generator'''
        Log.debug('post_process: {0}'.format(generate_rows))
        return generate_rows

    def execute(self):
        flatten_rows = partial(dp.flatten_json_struct,
                               count_fields=self.count_fields,
                               datetime_fields=self.datetime_fields)
        http_req = self.http_request()
        generate_rows = ({k:v for k,v in flatten_rows(x)}
                         for x in self.pre_process(http_req))
        return self.post_process(generate_rows)

class PivotCommand(BaseCommand):

    @abc.abstractproperty
    def pivot_field(self):
        pass
        
    def pre_process(self, generate_data):
        '''Return a generator from the source generator including pivot on sprint names
           sprint is no longer a list within a row but each sprint signifies a row
        '''
        pivot_on = self.pivot_field
        for x in generate_data:
            if pivot_on in x and x[pivot_on]:
                pivots = copy.copy(x[pivot_on])
                del x[pivot_on]
                #print('> pivot on {0} sprints'.format(len(sprints)))
                '''Create new json object for each sprint'''
                for pivot in pivots:
                    #print('> next sprint: {0}'.format(sprint['name']))
                    y = {pivot_on: pivot}
                    y.update(x.copy())
                    yield y
            else:
                yield x
