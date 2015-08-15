#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
"""/etc/sysconfig/i18n formats:

LANG="en_US.UTF-8"
SYSFONT="latarcyrheb-sun16"
"""
import sos_analyzer.scanner.base as SSB


class Scanner(SSB.SinglePatternScanner):

    name = input_name = "etc/sysconfig/i18n"
    pattern = r'^(?P<option>[^=]+)="?(?P<value>\S+)"?.*$'

# vim:sw=4:ts=4:et:
