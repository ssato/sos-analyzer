#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.analyzer.base as Base
import re


def find_close_to_full_filesystems(workdir, limit=80, input="df.json"):
    """
    :see: ``sos_analyzer.scanner.df``
    """
    data = Base.load_scanned_data(workdir, input)
    if data:
        for d in data:
            used_rate = d.get("used_rate", 0)
            if used_rate and int(used_rate) > limit:
                yield d


class Analyzer(Base.Analyzer):

    name = "filesystem"

    def analyze(self, *args, **kwargs):
        cfses = list(find_close_to_full_filesystems(self.workdir))

        return dict(close_to_full_filesystems=cfses)

# vim:sw=4:ts=4:et:
