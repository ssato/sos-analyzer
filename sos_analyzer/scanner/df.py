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
/dev/sda3              2030768    353548   1572396  19% /
proc                         0         0         0   -  /proc
sysfs                        0         0         0   -  /sys
devpts                       0         0         0   -  /dev/pts
/dev/sdc1              8123168    526360   7177516   7% /var
/dev/sda8              2948908     71748   2724948   3% /tmp
/dev/sda7              3050060    249668   2642960   9% /opt
/dev/sda6              4061540   2909064    942832  76% /usr
/dev/sda5              4870688    141028   4478248   4% /var/crash
/dev/sdb1              1011448     17928    941312   2% /home
/dev/sda1               303344     20718    266965   8% /boot
tmpfs                  1956360         0   1956360   0% /dev/shm
none                         0         0         0   -  /proc/sys/fs/binfmt_misc
sunrpc                       0         0         0   -  /var/lib/nfs/rpc_pipefs
"""

FS_RE = r"^(?P<filesystem>\S+)\s+(?P<max_blocks>\d+)\s+" + \
        r"(?P<used_blocks>\d+)\s+(?P<free_blocks>\d+)\s+" + \
        r"(?:(?P<used_rate>\d+)%|-)\s+(?P<mount_point>\S+)$"


class Scanner(SSB.SinglePatternScanner):

    name = input_name = "df"
    ignore_pattern = r"^(?:\#|[^a-z/]).*$"
    pattern = FS_RE

# vim:sw=4:ts=4:et:
