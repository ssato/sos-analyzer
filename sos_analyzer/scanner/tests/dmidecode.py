#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.dmidecode as TT
import sos_analyzer.tests.common as C
import os.path
import random
import re
import unittest


CURDIR = os.path.dirname(__file__)
INPUT_0 = os.path.join(CURDIR, "rhel-6-client-1.dmidecode.txt")
INPUT_1 = os.path.join(CURDIR, "rhel-6-server-1.dmidecode.txt")


def ri(hreg, line):
    return "regex=%s, line=%s" % (hreg, line)


class Test_00_regexes(unittest.TestCase):

    def setUp(self):
        self.lss = [[l.rstrip() for l in open(f).readlines()
                     if l.rstrip()] for f in (INPUT_0, INPUT_1)]

    def test_00_header_regexes(self):
        hregs = (TT.HEADER_BEGIN_RE, TT.HEADER_SMBIOS_RE,
                 TT.HEADER_STRUCTURES_RE, TT.HEADER_END_RE)

        for ls in self.lss:
            for i, hreg in enumerate(hregs):
                self.assertTrue(re.match(hreg, ls[i]), ri(hreg, ls[i]))

                for l in random.sample(ls[i + 1:], 3):
                    self.assertFalse(re.match(hreg, l), ri(hreg, l))

    def test_10_entry_header_regexes(self):
        for ls in self.lss:
            for i, l in enumerate(ls):
                if not l.startswith("Handle "):
                    continue

                self.assertTrue(re.match(TT.HANDLE_RE, l),
                                ri(TT.HANDLE_RE, l))
                next_l = ls[i + 1]
                m = re.match(TT.TABLE_END, next_l) or \
                    re.match(TT.ENTRY_HEADER, next_l) or \
                    re.match(TT.INACTIVE_ENTRY, next_l)
                self.assertTrue(m, ri("<entry_header_regexes>", next_l))

    def test_20_entry_data_regexes(self):
        for ls in self.lss:
            for i, l in enumerate(ls):
                if not re.match(r"^\s+.*$", l):
                    continue  # skip headers.

                if ':' in l:  # inline key, value or multilines key data:
                    if l.endswith(':'):
                        self.assertTrue(re.match(TT.MULTILINES_DATA_BEGIN, l),
                                        ri(TT.MULTILINES_DATA_BEGIN, l))
                    else:
                        self.assertTrue(re.match(TT.INLINE_DATA, l),
                                        ri(TT.INLINE_DATA, l))
                else:
                    self.assertTrue(re.match(TT.MULTILINES_DATA, l),
                                    ri(TT.MULTILINES_DATA, l))


class Test_10_Scanner(unittest.TestCase):

    def setUp(self):
        self.datadir = CURDIR
        self.scanner0 = TT.Scanner(self.datadir, self.datadir, INPUT_0)
        self.scanner1 = TT.Scanner(self.datadir, self.datadir, INPUT_1)

    def test_20_scan_file(self):
        self.assertTrue(self.scanner0.scan_file())
        self.assertTrue(self.scanner1.scan_file())

    def test_30_run(self):
        self.scanner0.run()
        self.assertTrue(self.scanner0.result)
        self.assertTrue(os.path.exists(self.scanner0.output_path))
        self.assertTrue(self.scanner0.result.get("data", None))

        self.scanner1.run()
        self.assertTrue(self.scanner1.result)
        self.assertTrue(os.path.exists(self.scanner1.output_path))
        self.assertTrue(self.scanner1.result.get("data", None))

# vim:sw=4:ts=4:et:
