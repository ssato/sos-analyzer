#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.tests.common as C
import sos_analyzer.cli as TT
import unittest


class Test_99_effeceful_functions(unittest.TestCase):

    def test_99_main__show_help_for_empty_args(self):
        self.assertNotEquals(TT.main(["./sos_analyzer", ]), 0)

# vim:sw=4:ts=4:et:
