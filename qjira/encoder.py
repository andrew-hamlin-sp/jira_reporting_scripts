import six

def _encode(encoding, s):
    return six.text_type(s).encode(encoding, errors='ignore').decode(encoding)
