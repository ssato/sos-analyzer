#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging
import sos_analyzer.scanner.chkconfig


#TODO: Pluggable scanners.
#
#import pkg_resources
#for e in pkg_resources.iter_entry_points("sos_analyzer_scanners"):
#    try:
#        SCANNERS.append(e.load())
#    except ImportError:
#        logging.warn("Could not load and append: " + str(e))
#        continue

SCANNERS = [sos_analyzer.scanner.chkconfig.Scanner, ]

# workdir, datadir, input_name=None, name=None, conf=None, subdir=SUBDIR):

def make_scanners_g(workdir, datadir, conf=None, scanners=SCANNERS):
    """
    :param workdir: Working dir to save results
    :param datadir: Data dir where input data file exists
    :param conf: A dict object holding scanners's configurations
    """
    for sc in scanners:
        yield sc(workdir, datadir, conf=conf)


def list(workdir, datadir, conf=None, scanners=SCANNERS):
    """
    :param workdir: Working dir to save results
    :param datadir: Data dir where input data file exists
    :param conf: A dict object holding scanners's configurations
    """
    return [sc for sc in make_scanners_g(workdir, datadir, conf, scanners)
            if sc.enabled]


# vim:sw=4:ts=4:et:
