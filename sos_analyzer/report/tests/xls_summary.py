#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import (
    ANALYZER_RESULTS_SUBDIR, REPORTS_SUBDIR, SUMMARY_JSON
)
import sos_analyzer.report.xls_summary as TT
import sos_analyzer.tests.common as C

import os.path
import os
import shutil
import unittest


CURDIR = os.path.dirname(__file__)
SAMPLE_SUMMARY_JSON = os.path.join(CURDIR, "00_example_results-summary.json")


class Test_00_XlsSummaryGenerator(unittest.TestCase):

    def setUp(self):
        self.workdir = C.setup_workdir()
        self.inputs_dir = os.path.join(self.workdir, ANALYZER_RESULTS_SUBDIR)
        self.outputs_dir = os.path.join(self.workdir, REPORTS_SUBDIR)

        os.makedirs(self.inputs_dir)
        shutil.copyfile(SAMPLE_SUMMARY_JSON,
                        os.path.join(self.inputs_dir, SUMMARY_JSON))

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_00_run(self):
        generator = TT.XlsSummaryGenerator(self.inputs_dir, self.outputs_dir)
        self.assertTrue(isinstance(generator, TT.XlsSummaryGenerator))

        generator.run()

        outpath = os.path.join(self.outputs_dir,
                               SUMMARY_JSON.replace(".json", ".xls"))
        self.assertTrue(os.path.exists(outpath))

# vim:sw=4:ts=4:et:
