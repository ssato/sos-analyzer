#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.tests.common as C
import sos_analyzer.scanner.chkconfig as TT
import os.path
import random
import unittest


CURDIR = os.path.dirname(__file__)
INPUT_0 = os.path.join(CURDIR, "rhel-6-client-1.chkconfig.txt")


def get_random_line(input=INPUT_0, start=0, end=None):
    ls = open(input).read().splitlines()
    if end is None:
        end = len(ls) - 1  # index starts w/ '0'.

    while True:
        l = ls[random.randint(start, end)]
        if l:
            return l


class Test_00_Scanner(unittest.TestCase):

    def setUp(self):
        self.datadir = CURDIR
        self.scanner = TT.Scanner(self.datadir, self.datadir, INPUT_0)

    def test_10_regexes(self):
        # FIXME: Hard-coded line numbers.
        line = get_random_line(end=35)
        #TT.logging.warn("line=" + line)
        self.assertTrue(self.scanner.match("svc", line), line)

        line = get_random_line(start=41)
        self.assertFalse(self.scanner.match("svc", line), line)
        self.assertTrue(self.scanner.match("xinetd_svc", line), line)

    def test_20_scan_file(self):
        self.assertTrue(self.scanner.scan_file())

    def test_30_run(self):
        self.scanner.run()
        self.assertTrue(self.scanner.result)
        self.assertTrue(os.path.exists(self.scanner.output_path))
        self.assertTrue(self.scanner.result.get("data", None))

# vim:sw=4:ts=4:et:
