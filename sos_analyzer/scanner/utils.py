#
# Utility rountines for scanners.
#
# Copyright (C) 2013 - 2015 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import re
import sos_analyzer.compat


DICT_MZERO = dict()


def compile_patterns(conf={}):
    """
    >>> cps = compile_patterns(dict(patterns=dict(aaa=r"([a-z]+)",
    ...                                           bbb=r"([0-9]+)")))
    >>> assert cps["aaa"].match("abc") is not None
    >>> assert cps["bbb"].match("123") is not None
    """
    return dict((k, re.compile(v)) for k, v in
                sos_analyzer.compat.iteritems(conf.get("patterns",
                                                       DICT_MZERO)))


def kvs_to_a_dict(kvs):
    """
    >>> kvs = dict(key="abc", value=123)
    >>> kvs_to_a_dict(kvs)
    {'abc': 123}
    """
    k = kvs["key"]
    v = kvs["value"]
    return {k: v}

# vim:sw=4:ts=4:et:
