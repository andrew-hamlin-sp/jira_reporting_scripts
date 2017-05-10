'''data.py - process a jira issue'''

import re
import dateutil.parser

from .log import Log

def calculate_rows(issue, pivot=None):
    '''factory method processing an issue into 1..N rows'''
    return DataProcessor(issue, pivot=pivot).rows()

def _generate_name(*args):
    return '_'.join([str(a) for a in args])

def _create_history_status_entry(hst):
    field_name = hst['field']
    normalized_string = hst['toString'].replace(' ', '')
    created_date = dateutil.parser.parse(hst['created']).date()
    return _generate_name(field_name,normalized_string),created_date

def _extract_sprint(sprint):
    m = re.search('\[(.+)\]', sprint)
    if m:
        d = dict(e.split('=') for e in m.group(1).split(','))
        for n in ('startDate','endDate','completeDate'):
            try:
                d[n] = dateutil.parser.parse(d[n]).date()
            except ValueError:
                d[n] = None
        return d
    raise ValueError

def _transform_dict(name, value):
    for col in [(_generate_name(name, k1),v1) for k1, v1 in value.items()]:
        yield col
    
def _transform_list(name, value):
    for idx,item in enumerate(value):
        for col in [(_generate_name(name, idx, k1),v1) for k1, v1 in item.items()]:
            yield col
    return

# flatten the dictionary object `json`
def _mapper(name, value):
    value_type = type(value)

    #print('>> name {} value_type {}'.format(name, value_type))

    if value_type is dict:
        for subitem in _transform_dict(name, value):
            yield subitem
    elif value_type is list:
        for subitem in _transform_list(name, value):
            yield subitem
    else:
        yield name, value

    return

class DataProcessor:

    def __init__(self, data, pivot=None):
        ''' process an jira issue'''
        self._pivot_field = pivot
        
        self._data = self._pre_process(data)

        self._build_pivots()
            
        self._build_cols()

        self._build_rows()

    def _pre_process(self, data):
        ''' clean up some custom fields'''

        # -- begin pre-process
        # update dictionary to reflect known names for custom fields
        if data['fields'].get('customfield_10016'):
            data['fields']['sprint'] = [sprint for sprint in map(_extract_sprint, data['fields']['customfield_10016'])]
            del data['fields']['customfield_10016']

        if data['fields'].get('customfield_10109'):
            data['fields']['story_points'] = data['fields']['customfield_10109']
            del data['fields']['customfield_10109']
        # -- end pre-process
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
                        pivot_item = {k:v for k,v in _mapper(pivot_field, src_item)}
                        pivots.append(pivot_item)
                    del data['fields'][pivot_field]
                    #print('> pivots {}'.format(pivots))
            except KeyError:
                pass

        Log.debug('pivots {}'.format(pivots))
        self._pivots = pivots

    def _build_cols(self):
        field_cols = self._extract_fields()
        history_cols = self._extract_histories()

        cols = field_cols.copy()
        cols.update(history_cols)
        Log.debug('cols {}'.format(cols))
        self._cols = cols
        
    def _extract_fields(self):
        data = self._data
        cols = dict(issue_key=data['key'])

        for key,val in data['fields'].items():
            if not val: continue
            cols.update({k:v for k,v in _mapper(key,val)})
            
        #print('> cols {}'.format(cols))
        return cols

    def _extract_histories(self):
        data = self._data
        ret_status = {}

        try:
            histories = sorted(data['changelog']['histories'], key=lambda x: x['created'])
            #print('>> sorted history {}'.format(histories))

            for history in histories:
                for history_item in history['items']:
                    if history_item['field'] == 'status':
                        history_item_status = dict(history_item.items(), created=history['created'])
                        ret_status.update({_create_history_status_entry(history_item_status)})

        except KeyError:
            pass
        
        #print('>> ret_status {}'.format(ret_status))
        return ret_status

    def _build_rows(self):
        rows = []
        if self._pivot_field:
            for p in self._pivots:
                r = p.copy()
                r.update(self._cols)
                rows.append(r)            
        else:
            rows.append(self._cols)

        self._rows = rows
                
    def rows(self):
        return self._rows
