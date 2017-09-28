import io
import sys
import csv
import locale
import six
import codecs
from functools import partial

def _encode(encoding, s):
    return six.text_type(s).encode(encoding, errors='ignore').decode(encoding)


def write(f, command, encoding):
    '''Write command output to csv file.

    Required arguments:
    out - the output file descriptor
    command - the command object
    encoding - the output encoding to use
    '''
    writer = None
    fieldnames = lambda row: [_encode(encoding, s) for s in command.expand_header(row.keys())]

    for row in command.execute():
        if not writer:
            writer = csv.DictWriter(f, fieldnames=fieldnames(row),
                                    dialect='excel',
                                    extrasaction='ignore')
            writer.writeheader()

        writer.writerow({k: _encode(encoding, v) for k, v in row.items()})

    if hasattr(writer, 'close'):
        writer.close()
