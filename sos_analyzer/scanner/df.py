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

FS_RE = r"^(?P<filesystem>\S+)\s+(?P<max_blocks>\d+)\s+" + \
        r"(?P<used_blocks>\d+)\s+(?P<free_blocks>\d+)\s+" + \
        r"(?:(?P<used_rate>\d+)%|-)\s+(?P<mount_point>\S+)$"


class Scanner(SSB.SinglePatternScanner):

    name = input_name = "df"
    ignore_pattern = r"^(?:\#|[^a-z/]).*$"
    pattern = FS_RE

# vim:sw=4:ts=4:et:
