#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import anyconfig
import logging
import optparse
import os
import os.path
import sys

from sos_analyzer.globals import DATA_SUBDIR

import sos_analyzer.archive
import sos_analyzer.runner
import sos_analyzer.utils


LOGGER = logging.getLogger(__name__)

DEFAULTS = dict(loglevel=1, conf=None, workdir=None, analyze=True,
                report=False)

USAGE = """%prog [Options...] SOS_REPORT_ARCHIVE_PATH

Examples:
  %prog --workdir ./result /tmp/sosreport-host_abc_01-12345-67e056.tar.bz2"""


def option_parser(defaults=DEFAULTS, usage=USAGE):
    p = optparse.OptionParser(usage)
    p.set_defaults(**defaults)

    p.add_option("-C", "--conf",
                 help="Configuration file path or paths or its pattern "
                      "such as '/a/b/*.json'")
    p.add_option("-w", "--workdir",
                 help="Workding dir to save result. Computed and created "
                      "automatically by default.")
    p.add_option("", "--no-analyze", action="store_false",
                 help="Do not analyze (scanned) data")
    p.add_option("", "--report", action="store_true",
                 help="Generate reports. It must not be specified w/ "
                      "--no-analyze option")

    p.add_option("-s", "--silent", action="store_const", dest="loglevel",
                 const=0, help="Silent or quiet mode")
    p.add_option("-q", "--quiet", action="store_const", dest="loglevel",
                 const=0, help="Same as --silent option")
    p.add_option("-v", "--verbose", action="store_const", dest="loglevel",
                 const=2, help="Verbose mode")

    return p


def main(argv=sys.argv):
    p = option_parser()
    (options, args) = p.parse_args(argv[1:])

    sos_analyzer.utils.set_loglevel(options.loglevel)

    if not args:
        p.print_usage()
        return -1

    conf = anyconfig.load(options.conf) if options.conf else None

    if options.workdir:
        LOGGER.info("Try using working dir: %s", options.workdir)
        sos_analyzer.utils.setup_workdir(options.workdir)
    else:
        options.workdir = sos_analyzer.utils.setup_workdir()
        LOGGER.info("Created working dir: %s", options.workdir)

    tarfile = args[0]
    datadir = os.path.join(options.workdir, DATA_SUBDIR)

    if not os.path.exists(datadir):
        LOGGER.info("Create datadir: %s", datadir)
        os.makedirs(datadir)

    d = sos_analyzer.utils.find_dir_has_target(datadir, "sos_commands")
    if d:
        LOGGER.info("sosreport archive looks already extracted in %s", d)
        datadir = d
    else:
        LOGGER.info("Extract sosreport archive %s to %s", tarfile, datadir)
        sos_analyzer.archive.extract_archive(tarfile, datadir)

        d = sos_analyzer.utils.find_dir_has_target(datadir, "sos_commands")
        if d:
            LOGGER.info("Set datadir to %s", d)
            datadir = d
        else:
            LOGGER.error("No sosreport data found under %s", d)
            return -1

    sos_analyzer.runner.run_scanners(options.workdir, datadir, conf)

    if options.analyze:
        sos_analyzer.runner.run_analyzers(options.workdir, datadir, conf)
        sos_analyzer.runner.dump_collected_results(options.workdir)

        if options.report:
            sos_analyzer.runner.run_report_generators(options.workdir,
                                                      options.conf)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

# vim:sw=4:ts=4:et:
