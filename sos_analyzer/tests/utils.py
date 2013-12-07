#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.tests.common as C
import sos_analyzer.utils as TT
import logging
import os.path
import os
import unittest


class Test_00_pure_functions(unittest.TestCase):

    def test_10_to_log_level(self):
        self.assertEquals(TT.to_log_level(0), logging.WARN)
        self.assertEquals(TT.to_log_level(1), logging.INFO)
        self.assertEquals(TT.to_log_level(2), logging.DEBUG)

        self.assertRaises(AssertionError, TT.to_log_level, 3)
        self.assertRaises(AssertionError, TT.to_log_level, -1)

    def test_10_dic_get_recur(self):
        self.assertEquals(TT.dic_get_recur({}, "a.b.c"), None)
        self.assertEquals(TT.dic_get_recur(dict(a=1, ), "b"), None)
        self.assertEquals(TT.dic_get_recur(dict(a=1, ), "a.b.c"), None)
        self.assertEquals(TT.dic_get_recur({}, "a.b.c", -1), -1)
        self.assertEquals(TT.dic_get_recur(dict(a=1, ), "a"), 1)
        self.assertEquals(TT.dic_get_recur(dict(a=dict(b=dict(c=2, ), ), ),
                                           "a.b.c"),
                          2)
        self.assertEquals(TT.dic_get_recur(dict(a=dict(b=dict(c=2, ), ), ),
                                           "a.b.X", 10),
                          10)


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_find_dir_has_target_subdir(self):
        d = os.path.join(self.workdir, "a", "b", "c", "d", "e")
        os.makedirs(os.path.join(d, "aaa"))

        self.assertEquals(TT.find_dir_has_target(self.workdir, "aaa"),
                          d)
        self.assertEquals(TT.find_dir_has_target(self.workdir, "bbb"),
                          None)

# vim:sw=4:ts=4:et:
