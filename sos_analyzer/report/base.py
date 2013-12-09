#
# Base class for report generators.
#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import (
    LOGGER as logging, REPORTS_SUBDIR as SUBDIR
)

import sos_analyzer.compat as SC
import sos_analyzer.runnable as SR
import os
import os.path


DICT_MZERO = dict()


class ReportGenerator(SR.RunnableWithIO):

    name = "report_generator"

    def __init__(self, inputs_dir=None, inputs=None, outputs_dir=None,
                 name=None, conf=None, **kwargs):
        """
        :param inputs_dir: Path to dir holding inputs
        :param inputs: List of filenames, path to input files, glob pattern
            of filename or None; ex. ["a/b.txt", "c.txt"], "a/b/*.yml"
        :param name: Object's name
        :param conf: A maybe nested dict holding object's configurations
        """
        super(ReportGenerator, self).__init__(inputs_dir, inputs,
                                              outputs_dir, name, conf,
                                              **kwargs)

    def update_data(self, data, diff):
        """
        TODO: How to update data w/ each data loaded ?

        :param data: All data
        :param diff: Data loaded from each input
        """
        data.update(diff)
        return data

    def load_inputs(self):
        data = DICT_MZERO
        for f in self.inputs:
            p = os.path.join(self.inputs_dir, f)
            logging.info("Loading inputs to generate reports: " + p)
            try:
                d = SC.json.load(open(p))
                data = self.update_data(data, d)
            except Exception as e:
                logging.warn("Failed to load %s, reason=%s " % (p, str(e)))

        return data

    def process_data(self, data, *args, **kwargs):
        return data

    def gen_reports(self, data, *args, **kwargs):
        raise NotImplementedError("Child class must implement this!")

    def run(self, *args, **kwargs):
        if not os.path.exists(self.outputs_dir):
            os.makedirs(self.outputs_dir)

        logging.info("Generating report w/ " + self.name)
        self.gen_reports(self.process_data(self.load_inputs()))

# vim:sw=4:ts=4:et:
