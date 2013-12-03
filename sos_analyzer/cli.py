#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging, DATA_SUBDIR

import sos_analyzer.archive as SA
import sos_analyzer.compat as SC
import sos_analyzer.utils as SU
import codecs
import locale
import optparse
import os
import sys
import tempfile


_encoding = locale.getdefaultlocale()[1]

if SC.IS_PYTHON_3:
    import io

    _encoding = _encoding.lower()

    # FIXME: Fix the error, "AttributeError: '_io.StringIO' object has no
    # attribute 'buffer'".
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=_encoding)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=_encoding)
    except AttributeError:
        pass
else:
    sys.stdout = codecs.getwriter(_encoding)(sys.stdout)
    sys.stderr = codecs.getwriter(_encoding)(sys.stderr)

DEFAULTS = dict(loglevel=1, workdir=None)

USAGE = """%prog [Options...] SOS_REPORT_ARCHIVE_PATH

Examples:
  %prog --workdir ./result /tmp/sosreport-host_abc_01-12345-67e056.tar.bz2"""


def option_parser(defaults=DEFAULTS, usage=USAGE):
    p = optparse.OptionParser(usage)
    p.set_defaults(**defaults)

    p.add_option("-w", "--workdir",
                 help="Workding dir to save result. Computed and created "
                      "automatically by default.")

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

    if not options.workdir:
        options.workdir = tempfile.mkdtemp(dir="/tmp", prefix="sos_analyzer-")
        logging.info("Created working dir: " + options.workdir)

    tarfile = args[0]
    datadir = os.path.join(options.workdir, DATA_SUBDIR)

    if not os.path.exists(datadir):
        logging.info("Create datadir: " + datadir)
        os.makedirs(datadir)

    SA.extract_archive(tarfile, datadir)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

# vim:sw=4:ts=4:et:
