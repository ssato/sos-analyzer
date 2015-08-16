#
# Copyright (C) 2013 - 2015 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
""" /etc/cron.d/sysstat formats:

# run system activity accounting tool every 10 minutes
*/10 * * * * root /usr/lib64/sa/sa1 1 1
# generate a daily summary of process accounting at 23:53
53 23 * * * root /usr/lib64/sa/sa2 -A

"""
import sos_analyzer.scanner.base


CRON_RE = (r"^(?P<timedate>(?:[\d*/]+\s+){5})"
           r"(?P<username>\S+)\s+(?P<command>.+)$")


class Scanner(sos_analyzer.scanner.base.SinglePatternScanner):

    name = input_name = "etc/cron.d/sysstat"
    pattern = CRON_RE

# vim:sw=4:ts=4:et:
