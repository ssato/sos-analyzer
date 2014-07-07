#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
# from operator import itemgetter
import sos_analyzer.analyzer.base as Base
import re


def find_hw_error_suspects_g(workdir, pattern, input="var/log/messages.json"):
    """
    :see: ``sos_analyzer.scanner.var_log_messages``
    """
    reg = re.compile(pattern, re.IGNORECASE)
    data = Base.load_scanned_data(workdir, input)
    if data:
        for d in data:
            if reg.match(d.get("message", '')):
                yield d


def find_hw_error_suspects(workdir, pattern, input="var/log/messages.json"):
    """
    :see: ``sos_analyzer.scanner.var_log_messages``
    """
    # Maybe this is not necessary as data are already sorted by date.
    # return sorted(find_hw_error_suspects_g(workdir, pattern, input),
    #              key=itemgetter("date"))
    return list(find_hw_error_suspects_g(workdir, pattern, input))


class Analyzer(Base.Analyzer):

    name = "hardware"
    error_msg_pattern = r"(?:i/o|memory|ecc|correct)"

    def analyze(self, *args, **kwargs):
        error_msg_re = self.getconf("error_msg_pattern",
                                    self.error_msg_pattern)
        hw_errors = find_hw_error_suspects(self.workdir, error_msg_re)

        return dict(hw_errors=hw_errors, )

# vim:sw=4:ts=4:et:
