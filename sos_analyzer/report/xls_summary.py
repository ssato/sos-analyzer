#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import (
    LOGGER as logging, SUMMARY_JSON, _
)
import sos_analyzer.report.base as SRB
import sos_analyzer.compat as SC
import anyconfig
import os
import os.path

try:
    import tablib
    _ENABLED = True
except ImportError:
    logging.warn("tablib is not available. Disable XlsSummaryGenerator.")
    _ENABLED = False


TABLIB_MISSING_MSG = _("""\
tablib is not available and this report generator is disabled: """)


class XlsSummaryGenerator(SRB.ReportGenerator):

    name = "xls_summary_generator"
    enabled = _ENABLED
    inputs = [SUMMARY_JSON]

    def process_data(self, *args, **kwargs):
        return anyconfig.load(self._mk_input_path(self.inputs[0]))

    def gen_reports(self, data, *args, **kwargs):
        if not self.enabled:
            logging.warn(TABLIB_MISSING_MSG + self.name)
            return

        dataset = tablib.Dataset()
        dataset.title = _("Results Summary")
        dataset.headers = (_("Category"), _("Check point"), _("Result"))

        for category, kvs in SC.iteritems(data):
            for k, v in SC.iteritems(kvs):
                if isinstance(v, (list, tuple)):
                    v = ", ".join(str(x) for x in v)
                elif isinstance(v, dict):
                    v = ", ".join("%s=%s" % (k, str(x)) for k, x in
                                  v.iteritems())
                else:
                    pass

                dataset.append((category, k, str(v)))

        book = tablib.Databook([dataset])
        fn = os.path.splitext(self.inputs[0])[0]
        outpath = self._mk_output_path(fn, ".xls")

        with open(outpath, 'wb') as out:
            # pylint: disable=no-member
            out.write(book.xls)
            # pylint: enable=no-member

# vim:sw=4:ts=4:et:
