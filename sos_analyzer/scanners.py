#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.asynccall
import sos_analyzer.scanner.chkconfig
import sos_analyzer.scanner.grub
import sos_analyzer.scanner.uname


#TODO: Pluggable scanners.
#
#import pkg_resources
#for e in pkg_resources.iter_entry_points("sos_analyzer_scanners"):
#    try:
#        SCANNERS.append(e.load())
#    except ImportError:
#        logging.warn("Could not load and append: " + str(e))
#        continue

SCANNERS = [sos_analyzer.scanner.chkconfig.Scanner,
            sos_analyzer.scanner.grub.Scanner,
            sos_analyzer.scanner.uname.Scanner]

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

    :return: A list of enabled scanner objects
    """
    return [sc for sc in make_scanners_g(workdir, datadir, conf, scanners)
            if sc.enabled]


def run(workdir, datadir, conf=None, timeout=20, scanners=SCANNERS):
    """
    :param workdir: Working dir to save results
    :param datadir: Data dir where input data file exists
    :param conf: A dict object holding scanners's configurations
    :param timeout: Timeout value in seconds for each scanner run
    :param scanners: A list of scanner objects to run
    """
    procs = [sos_analyzer.asynccall.call_async(sc.run) for sc
             in list(workdir, datadir, conf, scanners)]
    for p in procs:
        sos_analyzer.asynccall.stop_async_call(p, timeout, True)


# vim:sw=4:ts=4:et:
