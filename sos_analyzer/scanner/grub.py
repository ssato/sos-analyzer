#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging
import sos_analyzer.scanner.base as SSB


"""/boot/grub/grub.conf format:
#boot=/dev/sda
default=0
timeout=5
splashimage=(hd0,0)/grub/splash.xpm.gz
hiddenmenu
title Red Hat Enterprise Linux Server (2.6.18-238.el5)
        root (hd0,0)
        kernel /vmlinuz-2.6.18-238.el5 ro root=LABEL=/ rhgb quiet ...
        initrd /initrd-2.6.18-238.el5.img
title Red Hat Enterprise Linux Server (2.6.18-237.el5)
        root (hd0,0)
        kernel /vmlinuz-2.6.18-237.el5 ro root=LABEL=/ rhgb quiet ...
        initrd /initrd-2.6.18-237.el5.img
...
"""

INPUT = "boot/grub/grub.conf"
STATES = (IN_OPTIONS, AT_BOOT_ENTRY_TITLE, IN_BOOT_ENTRY) = \
    ("in_options", "at_boot_entry_title", "in_boot_entry")

OPTION_0_RE = r"^(?P<option>[a-z]+)=(?P<value>\S+).*$"
KERNEL_RE = r"^\s+kernel /vmlinuz-(?P<kernel>\S+) (?P<boot_option>.*)$"

CONF = dict(initial_state=IN_OPTIONS,
            ignore_empty_lines=1,
            # TODO: The 'root' and 'initrd' lines in each boot entry are simply
            # ignored currently.
            patterns=dict(comment=r"^#.*$",
                          options=r"^\S+$",
                          option_0=OPTION_0_RE,
                          option_1=r"^(?P<option>[a-z]+)$",
                          boot_entry_title=r"^title (?P<title>.*)$",
                          boot_entry_kerenl=KERNEL_RE))


class Scanner(SSB.BaseScanner):

    name = input_name = INPUT
    conf = CONF
    initial_state = IN_OPTIONS
    boot_entry_title = None

    def _update_state(self, state, line, i):
        """
        Update the internal state.

        :param state: A string or int represents the current state
        :param line: Content of the line
        :param i: Line number in the input file
        """
        if self.match("options", line):
            return IN_OPTIONS

        m = self.match("boot_entry_title", line)
        if m:
            # NOTE: It's kept until making up a boot entry dict later at
            # the 'kernel ...' line.
            self.boot_entry_title = m.groupdict().get("title", None)
            return AT_BOOT_ENTRY_TITLE

        if state == AT_BOOT_ENTRY_TITLE:
            return IN_BOOT_ENTRY  # Next state
        else:
            return state  # No change

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        if self.match("comment", line):
            return None

        if state == IN_OPTIONS:
            m = self.match("option_0", line)
            if m:
                return m.groupdict()

            m = self.match("option_1", line)
            if m:
                return m.groupdict()
            else:
                e = "Not a line of options? l=%s, lno=%d" % (line, i)
                logging.warn(e)

        elif state == IN_BOOT_ENTRY:
            m = self.match("boot_entry_kerenl", line)
            if m:
                d = m.groupdict()
                assert self.boot_entry_title is not None, \
                    "'kernel' line found but title is not set!: " + str(d)
                d["title"] = self.boot_entry_title
                self.boot_entry_title = None  # Reset it.
                return d
        else:
            pass

        return None

# vim:sw=4:ts=4:et:
