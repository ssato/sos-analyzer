#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.etc_hosts as TT
import sos_analyzer.tests.common as C
import os.path
import re
import unittest


CURDIR = os.path.dirname(__file__)
INPUT_0 = os.path.join(CURDIR, "etc_hosts_0.txt")


class Test_00_regexes(unittest.TestCase):

    def test_00_regexes(self):
        for l in open(INPUT_0).readlines():
            l = l.rstrip()
            if not l or re.match(TT.Scanner.ignore_pattern, l):
                continue

            self.assertTrue(re.match(TT.HOST_RE, l), "line=" + l)

# vim:sw=4:ts=4:et:
