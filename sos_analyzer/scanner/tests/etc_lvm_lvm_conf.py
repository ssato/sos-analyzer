#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.etc_lvm_lvm_conf as TT
import sos_analyzer.tests.common as C
import os.path
import unittest


CURDIR = os.path.dirname(__file__)
INPUT_0 = os.path.join(CURDIR, "rhel-6-client-1.etc_lvm_lvm.conf.txt")


class Test_00_Scanner(unittest.TestCase):

    def setUp(self):
        self.datadir = CURDIR
        self.scanner = TT.Scanner(self.datadir, self.datadir, INPUT_0)

    def test_10_regex__begin_section(self):
        lines = ["devices {", "allocation { ", "log {", "backup {",
                 "shell {", "global {"]  # activation, dmeventd, ...
        for line in lines:
            self.assertTrue(self.scanner.match("begin_section", line), line)

        lines = ["# metadata {", "# Event daemon", '    dir = "/dev"']
        for line in lines:
            self.assertFalse(self.scanner.match("begin_section", line), line)

    def test_12_regex__end_section(self):
        lines = ["}", "  } "]
        for line in lines:
            self.assertTrue(self.scanner.match("end_section", line), line)

        lines = ["metadata {", "# Event daemon", '  dir = "/dev"']
        for line in lines:
            self.assertFalse(self.scanner.match("end_section", line), line)

    def test_20_scan_file(self):
        self.assertTrue(self.scanner.scan_file())

    def test_30_run(self):
        self.scanner.run()
        self.assertTrue(self.scanner.result)
        self.assertTrue(os.path.exists(self.scanner.output_path))
        self.assertTrue(self.scanner.result.get("data", None))

# vim:sw=4:ts=4:et:
