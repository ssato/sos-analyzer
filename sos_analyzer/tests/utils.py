#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.tests.common as C
import sos_analyzer.utils as TT
import logging
import unittest


class Test_10_functions(unittest.TestCase):

    def test_10_to_log_level(self):
        self.assertEquals(TT.to_log_level(0), logging.WARN)
        self.assertEquals(TT.to_log_level(1), logging.INFO)
        self.assertEquals(TT.to_log_level(2), logging.DEBUG)

        self.assertRaises(AssertionError, TT.to_log_level, 3)
        self.assertRaises(AssertionError, TT.to_log_level, -1)

# vim:sw=4:ts=4:et:
