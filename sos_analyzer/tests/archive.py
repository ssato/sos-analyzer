#
# Copyright (C) 2013 Satoru SATOH <ssato at redhat.com>
# License: GPLv3+
#
import sos_analyzer.tests.common as C
import sos_analyzer.archive as TT
import sos_analyzer.shell as SS

import os
import os.path
import unittest


CURDIR = os.path.dirname(__file__)


class Test_10_effectful_functions(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_extract_archive(self):
        resultdir = os.path.join(self.workdir, "result")
        os.makedirs(resultdir)

        archive = os.path.join(resultdir, "foo.tar.gz")
        SS.run("tar zcvf %s .." % archive, CURDIR)

        TT.extract_archive(archive, resultdir)

# vim:sw=4 ts=4 et:
