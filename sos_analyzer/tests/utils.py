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


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_find_dir_having_target_subdir(self):
        d = os.path.join(self.workdir, "a", "b", "c", "d", "e")
        os.makedirs(os.path.join(d, "aaa"))

        self.assertEquals(TT.find_dir_having_target(self.workdir, "aaa"),
                          d)
        self.assertEquals(TT.find_dir_having_target(self.workdir, "bbb"),
                          None)

# vim:sw=4:ts=4:et:
