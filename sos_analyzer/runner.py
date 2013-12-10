#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import (
    LOGGER as logging, result_datadir, SUMMARY_JSON,
    ANALYZER_RESULTS_SUBDIR, REPORTS_SUBDIR,
)
import sos_analyzer.compat as SC
import sos_analyzer.asynccall
import sos_analyzer.analyzer.kernel
import sos_analyzer.analyzer.hardware
import sos_analyzer.analyzer.filesystem
import sos_analyzer.analyzer.i18n
import sos_analyzer.analyzer.ssh
import sos_analyzer.analyzer.system_service
import sos_analyzer.scanner.chkconfig
import sos_analyzer.scanner.df
import sos_analyzer.scanner.free
import sos_analyzer.scanner.grub
import sos_analyzer.scanner.installed_rpms
import sos_analyzer.scanner.runlevel
import sos_analyzer.scanner.uname
import sos_analyzer.scanner.etc_fstab
import sos_analyzer.scanner.etc_hosts
import sos_analyzer.scanner.etc_kdump_conf
import sos_analyzer.scanner.etc_ssh_sshd_config
import sos_analyzer.scanner.etc_sysconfig_i18n
import sos_analyzer.scanner.var_log_messages
import sos_analyzer.report.xls_summary

import os.path
import os


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
             sos_analyzer.analyzer.filesystem.Analyzer,
             sos_analyzer.analyzer.i18n.Analyzer,
             sos_analyzer.analyzer.system_service.Analyzer,
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
            sos_analyzer.scanner.etc_fstab.Scanner,
            sos_analyzer.scanner.etc_kdump_conf.Scanner,
            sos_analyzer.scanner.etc_ssh_sshd_config.Scanner,
            sos_analyzer.scanner.etc_sysconfig_i18n.Scanner,
            sos_analyzer.scanner.var_log_messages.Scanner,
            ]
REPORT_GENERATORS = [sos_analyzer.report.xls_summary.XlsSummaryGenerator,
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


def list_report_generators(workdir, conf=None, generators=REPORT_GENERATORS):
    """
    :param workdir: Working dir to save results
    :param datadir: Data dir where input data file exists
    :param conf: A dict object holding runners' configurations
    :param runners: A list of runnder classes

    :return: A list of enabled scanner or analyzer objects
    """
    resultsdir = os.path.join(workdir, ANALYZER_RESULTS_SUBDIR)
    outputsdir = os.path.join(workdir, REPORTS_SUBDIR)

    return [g(resultsdir, outputs_dir=outputsdir, conf=conf) for g
            in generators if g.enabled]


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


def run_report_generators(workdir, conf=None, timeout=20):
    """
    :param workdir: Working dir to save results
    :param conf: A dict object holding runners' configurations
    :param timeout: Timeout value in seconds for each runner run
    :param runners: A list of runnder classes
    """
    procs = [sos_analyzer.asynccall.call_async(r.run) for r
             in list_report_generators(workdir, conf)]
    for p in procs:
        sos_analyzer.asynccall.stop_async_call(p, timeout, True)


SUMMARY_JSON = "results-summary.json"


def load_results_g(workdir, summary_file=SUMMARY_JSON):
    """
    Load results under workdir.
    """
    topdir = result_datadir(workdir)
    for dirpath, dirnames, filenames in os.walk(topdir):
        # dirpath, dirnames, filenames
        for f in filenames:
            if f == summary_file:
                continue

            path = os.path.join(dirpath, f)
            try:
                logging.info("Loading result: " + path)
                data = SC.json.load(open(path))
                relpath = os.path.relpath(dirpath, topdir)

                yield (relpath, data)

            except Exception as e:
                logging.warn("Failed to load %s, reason=%s" % (path, str(e)))
                continue


def collect_results(workdir):
    return dict((relpath, data) for relpath, data in load_results_g(workdir))


def dump_collected_results(workdir, summary_file=SUMMARY_JSON):
    outpath = os.path.join(result_datadir(workdir), summary_file)
    all_results = collect_results(workdir)

    SC.json.dump(all_results, open(outpath, 'w'))

# vim:sw=4:ts=4:et:
