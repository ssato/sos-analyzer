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


def filepath_to_name(filepath):
    """
    >>> filepath_to_name("a/b/c.json")
    'a/b/c'
    >>> filepath_to_name("a/b/c/d")
    'a/b/c/d'
    """
    return os.path.splitext(filepath)[0]


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

    def input_to_key(self, input):
        return filepath_to_name(input)

    def load_inputs(self):
        data = DICT_MZERO
        for f in self.inputs:
            p = os.path.join(self.inputsdir, f)
            logging.info("Loading inputs to generate reports: " + p)
            try:
                d = SC.json.load(open(p))

                # TODO: How to update data w/ d ?
                n = self.input_to_key(f)
                data[n] = d
            except Exception as e:
                logging.warn("Failed to load: " + p)

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
