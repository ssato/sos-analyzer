#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
"""uname formats:
1:
    Linux foo.example.com 2.6.18-238.el5 #1 SMP Sun Dec 19 14:22:44 EST \
        2010 x86_64 x86_64 x86_64 GNU/Linux
2:
    Linux localhost.localdomain 3.11.9-300.fc20.x86_64 #1 SMP Wed Nov 20 \
        22:23:25 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux
"""
import sos_analyzer.scanner.base


UNAME_RE = r"^(?P<sysname>\S+) (?P<nodename>\S+) (?P<kernel_release>\S+) " + \
           r"(?P<kernel_version>.+) (?P<machine>\S+) (?P<processor>\S+) " + \
           r"(?P<os>\S+)"


class Scanner(sos_analyzer.scanner.base.SinglePatternScanner):

    name = input_name = "uname"
    pattern = UNAME_RE

# vim:sw=4:ts=4:et:
