#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.asynccall
import sos_analyzer.analyzer.kernel
import sos_analyzer.analyzer.hardware
import sos_analyzer.analyzer.ssh
import sos_analyzer.scanner.chkconfig
import sos_analyzer.scanner.df
import sos_analyzer.scanner.free
import sos_analyzer.scanner.grub
import sos_analyzer.scanner.installed_rpms
import sos_analyzer.scanner.runlevel
import sos_analyzer.scanner.uname
import sos_analyzer.scanner.etc_hosts
import sos_analyzer.scanner.etc_ssh_sshd_config
import sos_analyzer.scanner.var_log_messages


#TODO: Make analyzers and scanners pluggable and loaded automatically.
#
#import pkg_resources
#for e in pkg_resources.iter_entry_points("sos_analyzer_scanners"):
#    try:
#        SCANNERS.append(e.load())
#    except ImportError:
#        logging.warn("Could not load and append: " + str(e))
#        continue
ANALYZERS = [sos_analyzer.analyzer.kernel.Analyzer,
             sos_analyzer.analyzer.hardware.Analyzer,
             sos_analyzer.analyzer.ssh.Analyzer,
             ]
SCANNERS = [sos_analyzer.scanner.chkconfig.Scanner,
            sos_analyzer.scanner.df.Scanner,
            sos_analyzer.scanner.free.Scanner,
            sos_analyzer.scanner.grub.Scanner,
            sos_analyzer.scanner.installed_rpms.Scanner,
            sos_analyzer.scanner.runlevel.Scanner,
            sos_analyzer.scanner.uname.Scanner,
            sos_analyzer.scanner.etc_hosts.Scanner,
            sos_analyzer.scanner.etc_ssh_sshd_config.Scanner,
            sos_analyzer.scanner.var_log_messages.Scanner,
            ]


def make_runners_g(workdir, datadir, conf=None, runners=[]):
    """
    :param workdir: Working dir to save results
    :param datadir: Data dir where input data file exists
    :param conf: A dict object holding runners' configurations
    :param runners: A list of runnder classes
    """
    for r in runners:
        yield r(workdir, datadir, conf=conf)


def list_runnables(workdir, datadir, conf=None, runners=[]):
    """
    :param workdir: Working dir to save results
    :param datadir: Data dir where input data file exists
    :param conf: A dict object holding runners' configurations
    :param runners: A list of runnder classes

    :return: A list of enabled scanner or analyzer objects
    """
    return [r for r in make_runners_g(workdir, datadir, conf, runners)
            if r.enabled]


def run(workdir, datadir, conf=None, timeout=20, runners=[]):
    """
    :param workdir: Working dir to save results
    :param datadir: Data dir where input data file exists
    :param conf: A dict object holding runners' configurations
    :param timeout: Timeout value in seconds for each runner run
    :param runners: A list of runnder classes
    """
    procs = [sos_analyzer.asynccall.call_async(r.run) for r
             in list_runnables(workdir, datadir, conf, runners)]
    for p in procs:
        sos_analyzer.asynccall.stop_async_call(p, timeout, True)


def run_scanners(workdir, datadir, conf=None, timeout=20):
    """
    Alias of ``run`` to run scanners.
    """
    run(workdir, datadir, conf, timeout, SCANNERS)


def run_analyzers(workdir, datadir, conf=None, timeout=20):
    """
    Alias of ``run`` to run analyzers.
    """
    run(workdir, datadir, conf, timeout, ANALYZERS)

# vim:sw=4:ts=4:et:
