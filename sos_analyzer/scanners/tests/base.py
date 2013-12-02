#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.tests.common as C
import sos_analyzer.scanners.base as TT
import os.path
import logging
import unittest


CURDIR = os.path.dirname(__file__)


class Test_10_functions(unittest.TestCase):

    def test_10_dic_get_recur(self):
        self.assertEquals(TT.dic_get_recur({}, "a.b.c"), None)
        self.assertEquals(TT.dic_get_recur(dict(a=1, ), "b"), None)
        self.assertEquals(TT.dic_get_recur({}, "a.b.c", -1), -1)
        self.assertEquals(TT.dic_get_recur(dict(a=1, ), "a"), 1)
        self.assertEquals(TT.dic_get_recur(dict(a=dict(b=dict(c=2, ), ), ),
                                           "a.b.c"),
                          2)


CONF_0 = dict(a=1, b=2, patterns=dict(aaa=r"([a-z]+)", bbb=r"([0-9]+)"))


class Test_20_BaseScanner(unittest.TestCase):

    def setUp(self):
        self.scanner = TT.BaseScanner(CURDIR, conf=CONF_0)

    def test_10_getconf(self):
        self.assertEquals(self.scanner.getconf("a"), 1)

    def test_20_match(self):
        self.assertTrue(self.scanner.match("aaa", "abc"))
        self.assertTrue(self.scanner.match("bbb", "123"))

# vim:sw=4:ts=4:et:
