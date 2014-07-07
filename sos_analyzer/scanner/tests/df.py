#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.df as TT
import os.path
import re
import unittest


CURDIR = os.path.dirname(__file__)
INPUT_0 = os.path.join(CURDIR, "rhel-6-client-1.df.txt")


class Test_00_regexes(unittest.TestCase):

    def test_00_regexes(self):
        ls = [l.rstrip() for l in open(INPUT_0).readlines() if l.rstrip()]

        self.assertTrue(re.match(TT.FS_ML_0_RE, ls[1]), "line=" + ls[1])
        self.assertTrue(re.match(TT.FS_ML_1_RE, ls[2]), "line=" + ls[2])

        for l in ls[3:]:
            if re.match(TT.IGNORE_RE, l):
                continue

            self.assertTrue(re.match(TT.FS_SL_RE, l), "line=" + l)


class Test_10_Scanner(unittest.TestCase):

    def setUp(self):
        self.datadir = CURDIR
        self.scanner = TT.Scanner(self.datadir, self.datadir, INPUT_0)

    def test_20_scan_file(self):
        self.assertTrue(self.scanner.scan_file())

    def test_30_run(self):
        self.scanner.run()
        self.assertTrue(self.scanner.result)
        self.assertTrue(os.path.exists(self.scanner.output_path))
        self.assertTrue(self.scanner.result.get("data", None))

# vim:sw=4:ts=4:et:
