'''data.py - process a jira issue'''

import re
from dateutil import parser as date_parser

from .log import Log

re_prog = re.compile('[0-9]{4}\-[0-9]{2}\-[0-9]{2}T[0-9]{2}\:[0-9]{2}:[0-9]{2}\.[0-9]{3}\-[0-9]{4}')


def _generate_name(*args):
    return '_'.join([str(a) for a in args])

def _create_history_entry(hst):
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

def _extract_sprint(sprint):
    m = re.search('\[(.+)\]', sprint)
    if m:
        d = dict(e.split('=') for e in m.group(1).split(','))
        for n in ('startDate','endDate','completeDate'):
            try:
                the_date = date_parser.parse(d[n]).date()
                d[n]= the_date
            except ValueError:
                d[n] = None
        return d
    raise ValueError

def flatten_json_struct(data, count_fields=[], datetime_fields=[]):
    """data is a dict of nested JSON structures, returns a flattened array of tuples.
    skips entry when v == None
    """
    for k,v in data.items():
        if type(v) != dict and type(v) != list:
            if k in datetime_fields and re_prog.match(v):
                yield k, date_parser.parse(v).date()
            else:
                yield k, v                
        elif type(v) == list:
            if k in count_fields:
                yield k, len(v)
            else:
                new_data = { _generate_name(k,idx):val for idx,val in enumerate(v) }
                #print ('recursing %s' % new_data)
                for item in flatten_json_struct(new_data,
                                                count_fields=count_fields,
                                                datetime_fields=datetime_fields):
                    #print ('yielding flatted item %s %s', (item, type(item)))
                    yield item[0], item[1]            
        elif type(v) == dict:
            new_data = { _generate_name(k, k1): v1 for k1, v1 in v.items()}
            #print ('recursing %s' % new_data)
            for item in flatten_json_struct(new_data,
                                            count_fields=count_fields,
                                            datetime_fields=datetime_fields):
                #print ('yielding flatted item %s %s', (item, type(item)))
                yield item[0], item[1]

        
class DataProcessor:

    def __init__(self, pivot=None, reverse_sprints=False):
        ''' process an jira issue'''
        self._pivot_field = pivot
        self._reverse_sprints = reverse_sprints

    def transform(self, data):
        self._data = self._pre_process(data)
        self._build_pivots()
        self._build_cols()
        return self._generate_rows()

    def _pre_process(self, data):
        ''' clean up some custom fields'''
        # update dictionary to reflect known names for custom fields

        custom_field_map = [('customfield_10109','story_points'),
                            ('customfield_11101','design_doc_link'),
                            ('customfield_14300','testplan_doc_link'),
                            ('customfield_10017','epic_issuekey'),
                            ('customfield_10112','severity'),
                            ('customfield_10400','customer')]

        fields = data['fields']
        for s, d in custom_field_map:
            if fields.get(s):
                data['fields'][d] = fields[s]
                del data['fields'][s]

        # Sprint field must be converted from Java string representation to dict and sorted by start date
        if fields.get('customfield_10016'):
            data['fields']['sprint'] = [sprint for sprint in sorted(map(_extract_sprint, data['fields']['customfield_10016']), key=lambda x: x['startDate'], reverse=self._reverse_sprints)]
            del data['fields']['customfield_10016']

        return data

    def _build_pivots(self):
        data = self._data
        pivot_field = self._pivot_field
        pivots = []
        if pivot_field:
            try:
                # raises KeyError is bad pivot
                if data['fields'][pivot_field]:
                    for src_idx, src_item in enumerate(data['fields'][pivot_field]):
                        #print ('> src_idx {} is {}'.format(src_idx, src_item))
                        #pivot_item = {k:v for k,v in _mapper(pivot_field, src_item)}
                        # TODO replace for loop with dict comprehension !?
                        pivot_item = dict(flatten_json_struct({pivot_field: src_item}))
                        pivots.append(pivot_item)
                    del data['fields'][pivot_field]
                    #print('> pivots {}'.format(pivots))
            except KeyError:
                pass

        Log.verbose('pivots {}'.format(pivots))
        self._pivots = pivots

    def _build_cols(self):
        field_cols = self._extract_fields()
        # 1. extract all the history entries
        # 2. update status columns from history
        # 3. for design and test links, add created date column 
        history_cols = self._extract_histories()

        cols = field_cols.copy()
        if history_cols:
            cols.update(history_cols)
        Log.verbose('cols {}'.format(cols))
        self._cols = cols
        
    def _extract_fields(self):
        data = self._data
        cols = dict(issue_key=data['key'])
        cols.update(dict(flatten_json_struct(data['fields'],
                                             count_fields=['customer'],
                                             datetime_fields=['created',
                                                              'updated',
                                                              'lastViewed'])))
        return cols

    def _extract_histories(self):
        data = self._data

        if not data.get('changelog'):
            return None
        
        histories = sorted(data['changelog']['histories'], key=lambda x: x['created'])
        
        # 'field' seems to be standard attribute available in every item, 'fieldId' only exists in a sub-set
        return dict([_create_history_entry(dict(i, created=h['created']))
                     for h in histories for i in h['items'] if 'fieldId' in i])

    def _generate_rows(self):
        rows = []
        if self._pivot_field:
            for p in self._pivots:
                r = p.copy()
                r.update(self._cols)
                rows.append(r)            
        else:
            rows.append(self._cols)
        #print('Rows:', rows)
        return rows
