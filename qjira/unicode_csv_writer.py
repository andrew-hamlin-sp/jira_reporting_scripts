import csv

from .encoder import _encode


def write(f, command, encoding, delimiter=','):
    '''Write command output to csv file.

    Required arguments:
    out - the output file descriptor
    command - the command object
    encoding - the output encoding to use
    '''
    writer = None

    fieldnames = lambda row: [_encode(encoding, s) for s in command.expand_header(row)]

    for row in command.execute():
        if not writer:
            writer = csv.DictWriter(f, fieldnames=fieldnames(row),
                                    dialect='excel',
                                    delimiter=delimiter,
                                    extrasaction='ignore')
            writer.writeheader()

        writer.writerow({k: _encode(encoding, v) for k, v in row.items()})
