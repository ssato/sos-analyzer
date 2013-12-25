#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.base as SSB


# ex. 'N 3', see runlevel(8)
MATCH_RE = r"^((?P<prev_runlevel>N|\d)\s+)?(?P<cur_runlevel>\d|unknown)$"
INPUTS = "sos_commands/startup/runlevel"


class Scanner(SSB.SinglePatternScanner):

    name = input_name = INPUTS
    pattern = MATCH_RE


class Scanner2(SSB.StatelessScanner):

    inputs = INPUTS
    match_patterns = [MATCH_RE]

# vim:sw=4:ts=4:et:
