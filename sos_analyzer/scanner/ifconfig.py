#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import re


"""ifconfig output formats:

0: old style (RHEL 6)
eth0      Link encap:Ethernet  HWaddr 52:54:00:12:20:11
          inet addr:192.168.122.78  Bcast:192.168.122.255  Mask:255.255.255.0
          inet6 addr: fe80::5054:ff:fe12:2011/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:133196 errors:0 dropped:0 overruns:0 frame:0
          TX packets:105583 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:95181042 (90.7 MiB)  TX bytes:12274444 (11.7 MiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:16436  Metric:1
          RX packets:3157 errors:0 dropped:0 overruns:0 frame:0
          TX packets:3157 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:985345 (962.2 KiB)  TX bytes:985345 (962.2 KiB)

1: new style (F20 beta)
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.155.199  netmask 255.255.255.0  broadcast 192.168.155.255
        inet6 fe80::5054:ff:fe05:1111  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:05:11:11  txqueuelen 1000  (Ethernet)
        RX packets 157  bytes 14973 (14.6 KiB)
        RX errors 0  dropped 11  overruns 0  frame 0
        TX packets 133  bytes 18898 (18.4 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 0  (Local Loopback)
        RX packets 4428  bytes 365613 (357.0 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4428  bytes 365613 (357.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

virbr0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
        inet 192.168.122.1  netmask 255.255.255.0  broadcast 192.168.122.255
        ether 52:54:00:13:6a:a7  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
"""

STATES = (IFACE_START, IN_IFACE_INFO, IP_NETWORK, IP6_NETWORK,
          IFACE_STATS, RX_PACKETS, TX_PACKETS, ETH_STATS,
          IFACE_BYTES, RX_ERRORS, TX_ERRORS) \
       = ("iface_start", "in_iface_info", "ip_network", "ip6_network",
          "iface_stats", "rx_packets", "tx_packets", "eth_stats",
          "iface_bytes", "rx_errors", "tx_errors")

# Examples:
#eth0      Link encap:Ethernet  HWaddr 52:54:00:12:20:11
#lo        Link encap:Local Loopback
#virbr0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
IFACE_START_RE = r"^(?P<iface>[^:\s]+):?\s+(?:" + \
                 r"(?:Link encap:(?P<link>\S+)\s+" + \
                 r"(?:(?:HWaddr (?P<hwaddr>\S+))|Loopback))|" + \
                 r"(?:flags=\d+<(?P<flags>[^>]+)>\s+mtu\s+(?P<mtu>\d+)))$"

# Examples:
# inet addr:127.0.0.1  Mask:255.0.0.0
# inet addr:192.168.122.78  Bcast:192.168.122.255  Mask:255.255.255.0
# inet 127.0.0.1  netmask 255.0.0.0
# inet 192.168.155.254  netmask 255.255.255.0  broadcast 192.168.155.255
IP_NETWORK_RE_0 = r"^\s+inet addr:(?P<ipaddr>[\d.]+)\s+" + \
                  r"(?:Bcast:(?P<broadcast>[\d.]+)\s+)?" + \
                  r"Mask:(?P<netmask>[\d.]+)$"
IP_NETWORK_RE_1 = r"^\s+inet (?P<ipaddr>[\d.]+)\s+" + \
                  r"netmask (?P<netmask>[\d.]+)" + \
                  r"(?:\s+broadcast (?P<broadcast>[\d.]+))?$"

## TBD:
CONF = dict(initial_state=IFACE_START,
            ignore_empty_lines=1,
            patterns=dict(iface_start=IFACE_START_RE,
                          ip_network_0=IP_NETWORK_RE_0,
                          ip_network_1=IP_NETWORK_RE_1))


## TBD: Not completed its implementation yet.
class Scanner(SSB.BaseScanner):

    name = input_name = "ifconfig"
    conf = CONF
    initial_state = IFACE_START
    iface_info = None

    def _update_state(self, state, line, i):
        """
        Update the internal state.

        :param state: A string or int represents the current state
        :param line: Content of the line
        :param i: Line number in the input file
        """
        raise NotImplementedError("FIXME")

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        raise NotImplementedError("FIXME")

# vim:sw=4:ts=4:et:
