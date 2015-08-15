#
# Base class for analyzers.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import logging
import os.path
import os

from sos_analyzer.globals import result_datadir, scanned_datadir

import sos_analyzer.compat as SC
import sos_analyzer.utils as SU


DICT_MZERO = dict()
LOGGER = logging.getLogger(__name__)


def load_scanned_data(workdir, input):
    """
    Load data scanner generated from original data.
    """
    f = os.path.join(scanned_datadir(workdir), input)
    if not os.path.exists(f):
        logging.warn("Could not find scanned data: " + f)
        return None

    data = SC.json.load(open(f)) or {}
    if not data or not data.get("data", False):
        logging.warn("No valid data found: " + f)
        return None

    return data["data"]


class Analyzer(object):

    name = "base"
    conf = DICT_MZERO

    def __init__(self, workdir, datadir, name=None, conf=None):
        self.datadir = datadir

        if name is not None:
            self.name = name

        if conf is not None and isinstance(conf, dict):
            self.conf = conf

        self.workdir = workdir
        self.resultdir = os.path.join(result_datadir(workdir), self.name)

        self.enabled = self.getconf("enabled", True)

    def getconf(self, key, fallback=None, key_sep='.'):
        """
        :param key: Key to get configuration
        :param fallback: Fallback value if the value for given key is not found
        :param key_sep: Separator char to represents hierarchized configuraion
        """
        return SU.dic_get_recur(self.conf, key, fallback, key_sep)

    def analyze(self, *args, **kwargs):
        raise NotImplementedError("Child class must implement this method!")

    def save_result(self, result, *args, **kwargs):
        if not os.path.exists(self.resultdir):
            os.makedirs(self.resultdir)

        result_json = os.path.join(self.resultdir, "result.json")
        logging.debug("Dump result: " + self.name)
        SC.json.dump(result, open(result_json, 'w'))

    def run(self, *args, **kwargs):
        result = self.analyze(*args, **kwargs)
        self.save_result(result, *args, **kwargs)

# vim:sw=4:ts=4:et:
