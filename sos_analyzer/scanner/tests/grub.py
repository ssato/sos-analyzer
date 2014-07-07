#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.grub as TT
import os.path
import unittest


CURDIR = os.path.dirname(__file__)
INPUT_0 = os.path.join(CURDIR, "rhel-6-client-1.boot_grub_grub.conf.txt")
LINES_0 = list(open(INPUT_0).readlines())


def get_line(line, filepath=INPUT_0, lines=LINES_0):
    if lines:
        return lines[line]
    else:
        list(open(filepath).readlines())[line]


class Test_00_Scanner(unittest.TestCase):

    def setUp(self):
        self.datadir = CURDIR
        self.scanner = TT.Scanner(self.datadir, self.datadir, INPUT_0)

    def test_10_regexes(self):
        # FIXME: Hard-coded line numbers.
        line = get_line(9)
        self.assertTrue(self.scanner.match("options", line), line)
        self.assertTrue(self.scanner.match("option_0", line), line)

        line = get_line(12)
        self.assertTrue(self.scanner.match("options", line), line)
        self.assertTrue(self.scanner.match("option_1", line), line)

        line = get_line(13)
        self.assertTrue(self.scanner.match("boot_entry_title", line), line)

        line = get_line(15)
        self.assertTrue(self.scanner.match("boot_entry_kerenl", line), line)

    def test_20_scan_file(self):
        self.assertTrue(self.scanner.scan_file())

    def test_30_run(self):
        self.scanner.run()
        self.assertTrue(self.scanner.result)
        self.assertTrue(os.path.exists(self.scanner.output_path))
        self.assertTrue(self.scanner.result.get("data", None))

# vim:sw=4:ts=4:et:
