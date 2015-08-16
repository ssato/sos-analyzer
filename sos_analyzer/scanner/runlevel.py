#
# Copyright (C) 2013 - 2015 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.base


# ex. 'N 3', see runlevel(8)
MATCH_RE = r"^((?P<prev_runlevel>N|\d)\s+)?(?P<cur_runlevel>\d|unknown)$"
INPUTS = "sos_commands/startup/runlevel"


class Scanner(sos_analyzer.scanner.base.SinglePatternScanner):

    name = input_name = INPUTS
    pattern = MATCH_RE


class Scanner2(sos_analyzer.scanner.base.StatelessScanner):

    inputs = INPUTS
    match_patterns = [MATCH_RE]

# vim:sw=4:ts=4:et:
