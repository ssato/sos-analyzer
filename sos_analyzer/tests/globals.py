#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.globals as TT
import logging
import unittest


class Test_00(unittest.TestCase):

    def test_00_getLogger(self):
        self.assertTrue(isinstance(TT.getLogger(), logging.Logger))

# vim:sw=4:ts=4:et:
