#
# Author: Satoru SATOH <ssato redhat.com>
# License: MIT
#
import sys


IS_PYTHON_3 = sys.version_info[0] == 3

if IS_PYTHON_3:
    import configparser
    from io import StringIO

    import io
    # Not all version of python 3.x has sys.stdout.buffer?
    #sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    def uopen(path, flag='rt'):
        if flag[-1] != 't':
            flag = flag + 't'
        return io.open(path, flag, encoding='UTF-8')

    def iteritems(d):
        return d.items()
else:
    import ConfigParser as configparser
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    import codecs

    def uopen(path, flag='r'):
        return codecs.open(path, flag, encoding='UTF-8')

    def iteritems(d):
        return d.iteritems()

try:
    import json
except ImportError:
    import simplejson as json

# vim:sw=4:ts=4:et:
