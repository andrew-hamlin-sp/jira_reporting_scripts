'''data.py - process a jira issue'''
import re
import six
from dateutil import parser as date_parser

from .log import Log

re_prog = re.compile('[0-9]{4}\-[0-9]{2}\-[0-9]{2}T[0-9]{2}\:[0-9]{2}:[0-9]{2}\.[0-9]{3}\-[0-9]{4}')

def _generate_name(*args):
    return '_'.join([six.text_type(a) for a in args])

def create_history(hst):
    '''Create a tuple of important info from a changelog history.'''
    if hst['fieldId'] == 'status':
        field_name = hst['field'].replace(' ', '')
        normalized_string = hst['toString'].replace(' ', '')
    else:
        field_name = hst['field'].replace(' ', '_').lower()
        normalized_string = 'changed'
    created_date = date_parser.parse(hst['created']).date()
    entry = _generate_name(field_name,normalized_string), created_date
    #print ('Entry;',entry)
    return entry

def extract_sprint(sprint):
    '''Return a dict object containing sprint details.'''
    m = re.search('\[(.+)\]', sprint)
    if m:
        d = dict(e.split('=') for e in m.group(1).split(','))
        for n in ('startDate','endDate','completeDate'):
            try:
                the_date = date_parser.parse(d[n]).date()
                d[n]= the_date
            except ValueError:
                d[n] = None
        #print('> extract_sprint returns: {0}'.format(d))
        return d
    raise ValueError

def flatten_json_struct(data, count_fields=[], datetime_fields=[]):
    """data is a dict of nested JSON structures, returns a flattened array of tuples.

    Skips entry when value is None
    """
    for k,v in data.items():
        if v and type(v) != dict and type(v) != list:
            if k in datetime_fields and re_prog.match(v):
                #print('> yielding date {0}'.format(k))
                yield k, date_parser.parse(v).date()
            else:
                #print('> yielding value {0}: {1}'.format(k, v))
                yield k, v
        elif type(v) == list:
            if k in count_fields:
                #print('> yielding count of {0}'.format(k))
                yield k, len(v)
            else:
                new_data = { _generate_name(k,idx):val for idx,val in enumerate(v) }
                #print ('recursing %s' % new_data)
                for item in flatten_json_struct(new_data,
                                                count_fields=count_fields,
                                                datetime_fields=datetime_fields):
                    #print('> yielding {0}: {1}'.format(item, type(item)))
                    yield item[0], item[1]            
        elif type(v) == dict:
            new_data = { _generate_name(k, k1): v1 for k1, v1 in v.items()}
            #print ('recursing %s' % new_data)
            for item in flatten_json_struct(new_data,
                                            count_fields=count_fields,
                                            datetime_fields=datetime_fields):
                #print('> yielding {0}: {1}'.format(item, type(item)))
                yield item[0], item[1]
