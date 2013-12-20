# -*- coding: utf-8 -*-
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import re


"""df output formats:
1:
Filesystem           1K-ブロック    使用   使用可 使用% マウント位置
/dev/mapper/vg_rhel6client1-lv_root
                       4684748   2668868   1777904  61% /
tmpfs                   510292         0    510292   0% /dev/shm
/dev/vda1               495844     73591    396653  16% /boot

2:
ファイルシス                 1K-ブロック       使用    使用可 使用% マウント位置
devtmpfs                         8164368          0   8164368    0% /dev
tmpfs                            8209916          0   8209916    0% /dev/shm
tmpfs                            8209916      21596   8188320    1% /run
tmpfs                            8209916          0   8209916    0% /sys/fs/cgroup
/dev/mapper/vg0-lv_root       1920455616  836477948 986401120   46% /
tmpfs                            8209916          0   8209916    0% /tmp
/dev/sda1                         194241     101223     78682   57% /boot
/dev/mapper/vg0_data-lv_data  1952559608 1187673728 764885880   61% /srv/data
"""

STATES = (AT_HEADER, IN_ENTRIES) = ("at_header", "in_entries")

FS_RE = r"^(?P<filesystem>[a-z/]\S+)"
FS_REST_RE = r"\s+(?P<max_blocks>\d+)\s+" + \
             r"(?P<used_blocks>\d+)\s+(?P<free_blocks>\d+)\s+" + \
             r"(?:(?P<used_rate>\d+)%|-)\s+(?P<mount_point>/\S*)$"

FS_ML_0_RE = FS_RE + r"$"
FS_ML_1_RE = r"^" + FS_REST_RE
FS_SL_RE = FS_RE + FS_REST_RE
IGNORE_RE = r"^\#.*$"

CONF = dict(initial_state=AT_HEADER,
            patterns=dict(ignore=IGNORE_RE,
                          fs_multilines_0=FS_ML_0_RE,
                          fs_multilines_1=FS_ML_1_RE,
                          fs_line=FS_SL_RE))


class Scanner(SSB.BaseScanner):

    name = input_name = "df"
    conf = CONF
    state = initial_state = AT_HEADER
    entry = {}

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        if self.state == AT_HEADER:  # Use self.state instead of state passed.
            self.state = IN_ENTRIES
            logging.debug("state changed: %s -> %s, line=%s" % (AT_HEADER,
                                                                IN_ENTRIES,
                                                                line))
            return None

        if self.match("ignore", line):
            #logging.debug("ignored: line=%s" % line)
            return None

        m = self.match("fs_line", line)
        if m:
            #logging.debug("line=%s, matched=<fs_line>" % line)
            return m.groupdict()

        m = self.match("fs_multilines_0", line)
        if m:
            self.entry = m.groupdict()
            #logging.debug("line=%s, matched=<fs_multilines_0>" % line)
            return None

        m = self.match("fs_multilines_1", line)
        if m:
            entry = self.entry.copy()
            entry.update(m.groupdict())
            self.entry = {}
            #logging.debug("line=%s, matched=<fs_multilines_1>" % line)
            return entry

        return None

# vim:sw=4:ts=4:et:
