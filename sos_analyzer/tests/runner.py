#
# Copyright (C) 2013 Satoru SATOH <ssato at redhat.com>
# License: GPLv3+
#
import sos_analyzer.tests.common as C
import sos_analyzer.runner as TT
import unittest


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_make_runners__minimum_args(self):
        datadir = "/tmp"  # Dummy

        TT.list_runnables(self.workdir, datadir)

    def test_10_make_scanners(self):
        datadir = "/tmp"  # Dummy

        TT.list_runnables(self.workdir, datadir, runners=TT.SCANNERS)

    def test_20_make_analyzers(self):
        datadir = "/tmp"  # Dummy

        TT.list_runnables(self.workdir, datadir, runners=TT.ANALYZERS)

# vim:sw=4:ts=4:et:
