#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB


"""/proc/meminfo format:

MemTotal:      3912720 kB
MemFree:         29140 kB
Buffers:        506496 kB
Cached:        3012364 kB
SwapCached:          0 kB
Active:         803384 kB
Inactive:      2802356 kB
HighTotal:           0 kB
HighFree:            0 kB
LowTotal:      3912720 kB
LowFree:         29140 kB
SwapTotal:     6289436 kB
SwapFree:      6289436 kB
Dirty:           17220 kB
Writeback:           0 kB
AnonPages:       86764 kB
Mapped:          27040 kB
Slab:           234516 kB
PageTables:      11432 kB
NFS_Unstable:        0 kB
Bounce:              0 kB
CommitLimit:   8245796 kB
Committed_AS:   716124 kB
VmallocTotal: 34359738367 kB
VmallocUsed:    265936 kB
VmallocChunk: 34359471863 kB
HugePages_Total:     0
HugePages_Free:      0
HugePages_Rsvd:      0
Hugepagesize:     2048 kB
"""

class Scanner(SSB.SinglePatternScanner):

    name = input_name = "proc/meminfo"
    pattern = r"^(?P<key>[^:]+):\s+(?P<value>\d+)(?: (?P<unit>\S+))?$"

# vim:sw=4:ts=4:et:
