# -*- coding: utf-8 -*-
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.base as SSB


"""'installed-rpms' formats:
kbd-1.12-21.el5.x86_64                                      2012年02月08日 01時57分31秒
kcc-2.3-24.2.2.x86_64                                       2012年02月08日 01時55分30秒
kernel-2.6.18-238.el5.x86_64                                2012年02月08日 01時58分39秒
kernel-devel-2.6.18-238.el5.x86_64                          2012年02月08日 01時56分48秒
"""

class Scanner(SSB.SinglePatternScanner):

    name = input_name = "uname"
    pattern = r"^(?P<rpm>\S+)\s+(?P<installed_date>\S+)$"

# vim:sw=4:ts=4:et:
