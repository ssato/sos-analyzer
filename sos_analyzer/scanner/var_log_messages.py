#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import re


"""/var/log/messages formats:

0:
Nov 24 09:39:04 localhost kernel: [58333.193033] ehci-pci 0000:00:1d.0: System wakeup enabled by ACPI
Nov 24 09:39:04 localhost kernel: [58333.203911] ehci-pci 0000:00:1d.0: power state changed by ACPI to D3cold
Nov 24 09:39:04 localhost kernel: [58333.204267] ehci-pci 0000:00:1a.0: System wakeup enabled by ACPI

1:
Nov  7 15:58:34 host-aa-01 xinetd[3789]: START: telnet pid=31697 from=192.168.1.30
Nov  7 15:58:40 host-aa-01 login: pam_unix(remote:session): session opened for user foo by (uid=0)
Nov  7 15:58:40 host-aa-01 login: LOGIN ON pts/1 BY foo FROM workstation-001
Nov  7 15:59:01 host-aa-01 crond[31785]: (abc) CMD (/usr/bin/uptime >> /var/logs/uptime.xxxxx.log)
"""

LOG_RE = r"^(?P<date>\S+\s+[0-9]{1,2} [0-9:]+) (?P<host>\S+) " + \
         r"(?P<from>[^:\[]+)(?:\[(?P<pid>\d+)\])?: (?P<message>.*)$"


class Scanner(SSB.SinglePatternScanner):

    name = input_name = "var/log/messages"
    pattern = LOG_RE

# vim:sw=4:ts=4:et:
