#
# Base class for analyzers.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging, result_datadir

import sos_analyzer.utils as SU
import os.path


DICT_MZERO = dict()


class Analyzer(object):

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

    def getconf(self, key, fallback=None, key_sep='.'):
        """
        :param key: Key to get configuration
        :param fallback: Fallback value if the value for given key is not found
        :param key_sep: Separator char to represents hierarchized configuraion
        """
        return SU.dic_get_recur(self.conf, key, fallback, key_sep)

    def analyze(self, *args, **kwargs):
        raise NotImplementedError("Child class must implement this method!")

# vim:sw=4:ts=4:et:
