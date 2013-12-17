#
# Copyright (C) 2013 Red Hat, Inc.
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import gettext
import logging
import os.path


PACKAGE = "sos_analyzer"
AUTHOR = 'Satoru SATOH <ssat@redhat.com>'
VERSION = "0.0.1"

_LOGGING_FORMAT = "%(asctime)s %(name)s: [%(levelname)s] %(message)s"

DATA_SUBDIR = "data"
SCANNER_RESULTS_SUBDIR = "scanned"
ANALYZER_RESULTS_SUBDIR = "results"
REPORTS_SUBDIR = "reports"

SUMMARY_JSON = "results-summary.json"


def scanned_datadir(workdir, subdir=SCANNER_RESULTS_SUBDIR):
    return os.path.join(workdir, subdir)


def result_datadir(workdir, subdir=ANALYZER_RESULTS_SUBDIR):
    return os.path.join(workdir, subdir)


def getLogger(name="sos_analyzer", format=_LOGGING_FORMAT,
              level=logging.WARNING, **kwargs):
    """
    Initialize custom logger.
    """
    logging.basicConfig(level=level, format=format)
    logger = logging.getLogger(name)

    h = logging.StreamHandler()
    h.setLevel(level)
    h.setFormatter(logging.Formatter(format))
    logger.addHandler(h)

    return logger


_ = gettext.translation(domain=PACKAGE,
                        localedir=os.path.join(os.path.dirname(__file__),
                                               "locale"),
                        fallback=True).ugettext


LOGGER = getLogger()

# vim:sw=4:ts=4:et:
