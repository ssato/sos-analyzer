#
# Base class for report generators.
#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import (
    LOGGER as logging, REPORTS_SUBDIR as SUBDIR,
    ANALYZER_RESULTS_SUBDIR as RES_SUBDIR
)

import sos_analyzer.compat as SC
import sos_analyzer.runnable as SR
import os
import os.path


DICT_MZERO = dict()


class ReportGenerator(SR.RunnableWithIO):

    name = "report_generator"
    inputs_dir = RES_SUBDIR

    def __init__(self, inputs_dir=None, outputs_dir=None, inputs=None,
                 name=None, conf=None, **kwargs):
        """
        :param inputs_dir: Path to dir holding inputs
        :param outputs_dir: Path to dir to save results
        :param inputs: List of filenames, path to input files, glob pattern
            of filename or None; ex. ["a/b.txt", "c.txt"], "a/b/*.yml"
        :param name: Object's name
        :param conf: A maybe nested dict holding object's configurations
        """
        super(ReportGenerator, self).__init__(inputs_dir, outputs_dir,
                                              inputs, name, conf, **kwargs)
        if outputs_dir is None:
            self.outputs_dir = os.path.join(self.inputs_dir, "..", SUBDIR)

    def process_data(self, *args, **kwargs):
        return None

    def gen_reports(self, data, *args, **kwargs):
        raise NotImplementedError("Child class must implement this!")

    def run(self, *args, **kwargs):
        if not os.path.exists(self.outputs_dir):
            os.makedirs(self.outputs_dir)

        logging.info("Generating report w/ " + self.name)
        self.gen_reports(self.process_data(*args, **kwargs), *args, **kwargs)

# vim:sw=4:ts=4:et:
