#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.analyzer.base as Base
import sos_analyzer.analyzer.filesystem as SAF
import os.path
import re


FLAGS = ["size", "device", "readlink_path", "group", "checksum",
         "capabilities", "mode", "user", "mtime"]


def list_modified_g(workdir, input="rpm-Va.json", flags=FLAGS):
    """
    :see: ``sos_analyzer.scanner.rpm_Va``
    """
    data = Base.load_scanned_data(workdir, input)
    if data:
        for d in data:
            ms = [(f, d[f]) for f in flags if d.get(f, '.') != '.']
            if ms:
                d["modified"] = ", ".join(m[0] for m in ms)

                yield d


class Analyzer(Base.Analyzer):

    name = "rpm"
    inputs = []

    def analyze(self, *args, **kwargs):
        return dict(modified_rpm_files=list(list_modified_g(self.workdir)),)

# vim:sw=4:ts=4:et:
