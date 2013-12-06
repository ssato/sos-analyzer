#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import re


"""'free' output formats:

             total       used       free     shared    buffers     cached
Mem:       1020588     630304     390284          0     111916     277500
-/+ buffers/cache:     240888     779700
Swap:      1015800       1048    1014752
"""

HEADER_RE = r"^\s+total\s+used\s+free\s+shared\s+.*$"
MEMORY_RE = r"^Mem:\s+(?P<memory_total>\d+)\s+(?P<memory_used>\d+)\s+" + \
            r"(?P<memory_free>\d+)\s+(?P<memory_shared>\d+)\s+" + \
            r"(?P<memory_buffers>\d+)\s+(?P<memory_cached>\d+)$"
CACHE_RE = r"^.+buffers/cache:\s+(?P<cache_used>\d+)\s+(?P<cache_free>\d+)$"
SWAP_RE = r"^Swap:\s+(?P<swap_total>\d+)\s+" + \
          r"(?P<swap_used>\d+)\s+(?P<swap_free>\d+)$"


class Scanner(SSB.MultiPatternsScanner):

    name = input_name = "free"
    ignore_pattern = HEADER_RE
    multi_patterns = (MEMORY_RE, CACHE_RE, SWAP_RE)

# vim:sw=4:ts=4:et:
