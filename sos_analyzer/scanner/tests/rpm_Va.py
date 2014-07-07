#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.rpm_Va as TT
import os.path
import re
import unittest


CURDIR = os.path.dirname(__file__)
INPUT_0 = os.path.join(CURDIR, "rhel-6-client-1.rpm-Va.txt")

PRELINK_LINES_0 = ["prelink: /usr/lib64/libyajl.so.1.0.7: at least "
                   "one of file's dependencies has changed since prelinking",
                   ]
MOD_LINES_0 = ["....L....  c /etc/pam.d/system-auth",
               "S.5....T.    "
               "/usr/lib/python2.6/site-packages/jinja2_cli/render.py",
               "S.5....T.    "
               "/usr/lib/python2.6/site-packages/jinja2_cli/render.pyc",
               "S.?......    /usr/lib64/libyajl.so.1.0.",
               ]
OTHER_LINES_0 = [
    "  /var/cache/swapi/7ddfd9ea3a8f9cd7d1f40d8a4709d4c1.tar.xz ...",
]


class Test_00_Scanner(unittest.TestCase):

    def setUp(self):
        self.datadir = CURDIR
        self.scanner = TT.Scanner(self.datadir, self.datadir, INPUT_0)

    def test_10_regexes(self):
        for line in PRELINK_LINES_0:
            self.assertTrue(re.match(TT.PRELINK_RE, line))

        for line in MOD_LINES_0:
            self.assertTrue(re.match(TT.MODIFIED_RE, line))

        for line in OTHER_LINES_0:
            self.assertTrue(re.match(TT.OTHER_RE, line))

    def test_20_scan_file(self):
        self.assertTrue(self.scanner.scan_file())

    def test_30_run(self):
        self.scanner.run()
        self.assertTrue(self.scanner.result)
        self.assertTrue(os.path.exists(self.scanner.output_path))
        self.assertTrue(self.scanner.result.get("data", None))

# vim:sw=4:ts=4:et:
