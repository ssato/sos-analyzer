#
# Base class for analyzers.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging, result_datadir

import os.path


DICT_MZERO = dict()


class BaseAnalyzer(object):

    name = "base"
    conf = DICT_MZERO

    def __init__(self, workdir, datadir, name=None, conf=None):
        self.datadir = datadir

        if name is not None:
            self.name = name

        if conf is not None and isinstance(conf, dict):
            self.conf = conf

        self.scanned_datadir = scanned_datadir(workdir)
        self.resultdir = os.path.join(result_datadir(workdir), self.name)

    def analyze(self, *args, **kwargs):
        pass

# vim:sw=4:ts=4:et:
