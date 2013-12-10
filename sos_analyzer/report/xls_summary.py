#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import (
    LOGGER as logging, SUMMARY_JSON
)
import sos_analyzer.report.base as SRB
import sos_analyzer.compat as SC
import os
import os.path

try:
    import tablib
    _ENABLED = True
except ImportError:
    logging.warn("tablib is not available. Disable XlsSummaryGenerator.")
    _ENABLED = False


OUTPUT = SUMMARY_JSON.replace(".json", ".xls")


class XlsSummaryGenerator(SRB.ReportGenerator):

    name = "xls_summary_generator"
    enabled = _ENABLED
    inputs = [SUMMARY_JSON]

    def gen_reports(self, data, *args, **kwargs):
        if not self.enabled:
            logging.warn("tablib is not available and this report "
                         "generator is disabled: " + self.name)
            return

        dataset = tablib.Dataset()
        dataset.headers = ("Category", "Check point", "Result")

        for category, kvs in SC.iteritems(data):
            for k, v in SC.iteritems(kvs):
                if isinstance(v, (list, tuple)):
                    v = ", ".join(v)

                dataset.append((category, k, str(v)))

        book = tablib.Databook([dataset])
        outpath = os.path.join(self.outputs_dir, OUTPUT)

        with open(outpath, 'wb') as out:
            out.write(book.xls)

# vim:sw=4:ts=4:et:
