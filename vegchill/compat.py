"""Python2 and 3 compatible layer
"""
from __future__ import print_function

import six

if six.PY2:
    FileNotFoundError = IOError
else:
    long = int
    unicode = str
