#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB


"""chkconfig format:
atd             0:off   1:off   2:off   3:on    4:on    5:on    6:off
auditd          0:off   1:off   2:on    3:on    4:on    5:on    6:off
blk-availability        0:off   1:on    2:on    3:on    4:on    5:on    6:off
    ...
udev-post       0:off   1:on    2:on    3:on    4:on    5:on    6:off
xinetd          0:off   1:off   2:off   3:on    4:on    5:on    6:off

xinetd based services:
        chargen-dgram:  off
        chargen-stream: off
        daytime-dgram:  off
"""

INPUT = "chkconfig"
STATES = (IN_SVCS, AT_XINETD_SVCS_START, IN_XINETD_SVCS) = \
    ("in_services", "at_xinetd_svcs_start", "in_xinetd_svcs")

REG_0 = r"^(?P<service>[a-zA-Z]\S+)" + \
        r"\s+0:(on|off)\s+1:(on|off)\s+2:(on|off)\s+3:(on|off)" + \
        r"\s+4:(on|off)\s+5:(on|off)\s+6:(on|off)$"
REG_1 = r"^\s+(?P<xinetd_service>[^:]+):\s+(?P<status>on|off)$"
REG_2 = r"^xinetd [^:]+:$"

CONF = dict(initial_state=IN_SVCS,
            ignore_empty_lines=1,
            patterns=dict(svc=REG_0, xinetd_svc=REG_1,
                          xinetd_svcs_start=REG_2))


class Scanner(SSB.BaseScanner):

    name = input_name = INPUT
    conf = CONF
    initial_state = IN_SVCS

    def _update_state(self, state, line, i):
        """
        Update the internal state.

        :param state: A string or int represents the current state
        :param line: Content of the line
        :param i: Line number in the input file
        """
        if self.match("xinetd_svcs_start", line):
            return AT_XINETD_SVCS_START

        if state == AT_XINETD_SVCS_START:
            return IN_XINETD_SVCS  # Next state
        else:
            return state  # No change

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        if state == IN_SVCS:
            m = self.match("svc", line)
            if m:
                t = m.groups()
                return dict(service=t[0], status=t[1:])
            else:
                e = "Not a line of normal service? l=%s, lno=%d" % (line, i)
                logging.warn(e)

        elif state == IN_XINETD_SVCS:
            m = self.match("xinetd_svc", line)
            if m:
                return m.groupdict()
            else:
                e = "Not a line of xinetd service? l=%s, lno=%d" % (line, i)
                logging.warn(e)
        else:
            pass

        return None

# vim:sw=4:ts=4:et:
