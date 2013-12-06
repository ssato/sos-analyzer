#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.base as SSB


class Scanner(SSB.SinglePatternScanner):

    name = input_name = "sos_commands/startup/runlevel"

    # ex. 'N 3', see runlevel(8) 
    pattern = r"^(?P<prev_runlevel>N|\d)\s+(?P<cur_runlevel>\d|unknown)$"

# vim:sw=4:ts=4:et:
