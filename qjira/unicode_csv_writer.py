import io
import sys
import csv
import locale
import six
import codecs
from functools import partial
from contextlib import closing

PY3 = sys.version_info > (3,)

def _open(out, encoding):
    '''Open the file with given encoding'''
    if hasattr(out, 'write'):
        return out
    elif PY3:
        return io.open(out, 'wt',
                       encoding=encoding, newline='')
    else:
        return io.open(out, 'wb')

def _encode(encoding, s):
    return six.text_type(s).encode(encoding, errors='ignore').decode(encoding)
    
def _write_encoded(f, command, encoding):
    encoder = partial(_encode, encoding)
    fieldnames = [encoder(s) for s in command.header]
    writer = csv.DictWriter(f, fieldnames=fieldnames,
                            dialect='excel', extrasaction='ignore')
    writer.writeheader()
    for row in command.execute():
        row = {k: encoder(v) for k, v in row.items()}
        writer.writerow(row)

def write(out, command, encoding='ASCII'):
    '''Write command output to csv file.

    Required arguments:
    command - the command object
    out - the output file descriptor

    Optional arguments:
    encoding - the output encoding to use
    '''
    with closing(_open(out, encoding=encoding)) as f:
        _write_encoded(f, command, encoding)

