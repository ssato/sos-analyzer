#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.tests.common as C
import sos_analyzer.scanner.uname as TT
import os.path
import os
import unittest


EXAMPLES = [
"Linux foo 2.6.18-238.el5 #1 SMP Sun Dec 19 14:22:44 EST 2010 x86_64 x86_64 x86_64 GNU/Linux",
"Linux localhost.localdomain 3.11.9-300.fc20.x86_64 #1 SMP Wed Nov 20 22:23:25 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux",
]


class Test_00_Scanner(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()
        self.datadir = os.path.join(self.workdir, "data")
        os.makedirs(self.datadir)
        self.inputs = []

        for i, u in enumerate(EXAMPLES):
            f = os.path.join(self.datadir, "uname.%d" % i)
            self.inputs.append(f)
            open(f, 'w').write(u + "\n")

        self.scanners = [TT.Scanner(self.workdir, self.datadir, f) for f
                         in self.inputs]

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_regexes(self):
        line = EXAMPLES[0]
        self.assertTrue(self.scanners[0].match("match_pattern", line), line)

    def test_20_scan_file(self):
        for sc in self.scanners:
            self.assertTrue(sc.scan_file())

    def test_30_run(self):
        for sc in self.scanners:
            sc.run()
            self.assertTrue(sc.result)
            self.assertTrue(os.path.exists(sc.output_path))
            self.assertTrue(sc.result.get("data", None))

# vim:sw=4:ts=4:et:
