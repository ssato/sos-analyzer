#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging, DATA_SUBDIR

import sos_analyzer.archive as SA
import sos_analyzer.runner as SR
import sos_analyzer.utils as SU

import anyconfig
import optparse
import os
import os.path
import sys
import tempfile


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
    p.add_option("", "--reprot", action="store_true",
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

    SU.set_loglevel(options.loglevel)

    if not args:
        p.print_usage()
        return -1

    conf = anyconfig.load(options.conf) if options.conf else None

    if options.workdir:
        logging.info("Try using working dir: " + options.workdir)
        SU.setup_workdir(options.workdir)
    else:
        options.workdir = SU.setup_workdir()
        logging.info("Created working dir: " + options.workdir)

    tarfile = args[0]
    datadir = os.path.join(options.workdir, DATA_SUBDIR)

    if not os.path.exists(datadir):
        logging.info("Create datadir: " + datadir)
        os.makedirs(datadir)

    d = SU.find_dir_has_target(datadir, "sos_commands")
    if d:
        logging.info("sosreport archive looks already extracted in " + d)
        datadir = d
    else:
        logging.info("Extract sosreport archive %s to %s" % (tarfile, datadir))
        SA.extract_archive(tarfile, datadir)

        d = SU.find_dir_has_target(datadir, "sos_commands")
        if d:
            logging.info("Set datadir to " + d)
            datadir = d
        else:
            logging.error("No sosreport data found under " + d)
            return -1

    SR.run_scanners(options.workdir, datadir, conf)

    if options.analyze:
        SR.run_analyzers(options.workdir, datadir, conf)
        SR.dump_collected_results(options.workdir)

        if options.report:
            SR.run_report_generators(options.workdir, options.conf)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

# vim:sw=4:ts=4:et:
