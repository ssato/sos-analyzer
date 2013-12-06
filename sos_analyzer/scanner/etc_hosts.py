#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import re


"""/etc/hosts format:
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

# comment ....
192.168.1.254 gw.example.com gw   # gateway ...
192.168.1.20 aaaa-host-012   # w/o FQDN
192.168.1.30 aaaa-host-030.example.com aaaa-host-030
"""

HOST_RE = r"^(?P<ip>[0-9.]+)\s+(?P<hostnames>[^#]+)(?:\s+#(?P<comment>.*))*$"


class Scanner(SSB.SinglePatternScanner):

    name = input_name = "etc/hosts"
    pattern = HOST_RE

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        x = super(Scanner, self).parse_impl(state, line, i, *args, **kwargs)
        if x:
            x["hostnames"] = x.get("hostnames", '').split()

        return x

# vim:sw=4:ts=4:et:
