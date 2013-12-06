#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import re


"""/etc/ssh/sshd_config format:

#Port 22
#Protocol 2,1
Protocol 2
#AddressFamily any
...
# Accept locale-related environment variables
AcceptEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES 
AcceptEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT 
...

# override default of no subsystems
Subsystem       sftp    /usr/libexec/openssh/sftp-server
"""

class Scanner(SSB.SinglePatternScanner):

    name = input_name = "etc/ssh/sshd_config"
    pattern = r"^(?P<config>[A-Z]\S+)\s+(?P<value>\S.*)$"

# vim:sw=4:ts=4:et:
