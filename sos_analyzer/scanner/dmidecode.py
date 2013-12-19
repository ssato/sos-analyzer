#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import sos_analyzer.scanner.utils as SSU
import sos_analyzer.compat as SC


"""dmidecode format:

* test example: sos_analyzer/scanner/tests/rhel-6-client-1.dmidecode.txt
* see also:
  * dmidecode-2.11/dmidecode.c:dmi_decode()
"""

HEADER_BEGIN_RE = r"^# dmidecode (?P<dmidecode_version>(?:[\d.])+)$"
HEADER_SMBIOS_RE = r"^SMBIOS (?P<smbios_version>[\d.]+) present.$"
HEADER_STRUCTURES_RE = r"(?P<nstructures>\d+) structures occupying " + \
                       r"(?P<structures_byte>\d+) bytes.$"
HEADER_END_RE = r"^Table at (?P<table_at>0x\S+)$"
HANDLE_RE = r"^Handle (?P<handle_addr>0x\S+), " + \
            r"DMI type (?P<handle_type>\d+), (?P<handle_length>\d+) bytes"

TABLE_END = r"^End Of Table$"
INACTIVE_ENTRY = r"^Inactive$"

ENTRY_HEADER = r"^(?P<title>(?:(?:\S+) )+(?:\S+))$"
ENTRY_DATA_RE = r"^[\t]+.*$"
INLINE_DATA = r"^[\t]{1}(?P<key>[^:]+):\s+(?P<value>.+)$"
MULTILINES_DATA_BEGIN = r"^[\t]{1}(?P<key>[^:]+):$"
MULTILINES_DATA = r"^[\t]{2}(?P<value>.+)$"

STATES = (IN_HEADER, IN_ENTRY_HEADER, IN_ENTRY_DATA) = \
         ("in_header", "in_entry_header", "in_entry_data")

CONF = dict(initial_state=IN_HEADER,
            ignore_empty_lines=1,
            patterns=dict(header_begin=HEADER_BEGIN_RE,
                          header_smbios=HEADER_SMBIOS_RE,
                          header_structures=HEADER_STRUCTURES_RE,
                          header_end=HEADER_END_RE,
                          handle=HANDLE_RE,
                          table_end=TABLE_END,
                          inactive_entry=INACTIVE_ENTRY,
                          entry_header=ENTRY_HEADER,
                          entry_data=ENTRY_DATA_RE,
                          inline_data=INLINE_DATA,
                          multilines_data_begin=MULTILINES_DATA_BEGIN,
                          multilines_data=MULTILINES_DATA))

ENTRY_DATA_KEY = "data"


class Scanner(SSB.BaseScanner):

    name = input_name = "dmidecode"
    conf = CONF
    initial_state = IN_HEADER
    entry = {}  # Hold space.

    def _update_state(self, state, line, i):
        """
        Update the internal state.

        :param state: A string or int represents the current state
        :param line: Content of the line
        :param i: Line number in the input file
        """
        if self.match("handle", line):
            return IN_ENTRY_HEADER
        elif self.match("entry_data", line):
            return IN_ENTRY_DATA
        else:
            return state  # No change

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        if state == IN_HEADER:
            m = self.match("header_begin", line) or \
                self.match("header_smbios", line) or \
                self.match("header_structures", line)
            if m:
                self.entry.update(m.groupdict())
                header = None  # Keep parsing header...
            else:
                m = self.match("header_end", line)
                if m:
                    header = self.entry.copy()
                    header.update(m.groupdict())
                else:
                    logging.warn("Header does not look end correctly!")
                    header = self.entry.copy()

                self.entry = {}  # reset it to put entries data later.

            return header

        elif state == IN_ENTRY_HEADER:
            m = self.match("handle", line)
            if m:
                prev_entry = self.entry.copy()
                self.entry = m.groupdict()  # start keeping data of this entry.

                return prev_entry

            self.entry[ENTRY_DATA_KEY] = []  # Initialize the list to put data.
            self.state = self._update_state(IN_ENTRY_DATA, line, i)

            # Find a couple of special cases first:
            m = self.match("table_end", line)
            if m:
                return self.entry.copy()  # This should be the final one.

            m = self.match("inactive_entry", line)
            if m:
                entry = self.entry.copy()
                entry["inactive"] = True
                self.entry = {}

                return entry

            # Normal cases:
            m = self.match("entry_header", line)
            if m:
                self.entry.update(m.groupdict())
            else:
                logging.warn("Failed to parse entry header: "
                             "line_no=%d, line=%s" % (i, line))

        else:
            m = self.match("inline_data", line)
            if m:
                kvdata = SSU.kvs_to_a_dict(m.groupdict())
                self.entry[ENTRY_DATA_KEY].append(kvdata)

                return None

            m = self.match("multilines_data_begin", line)
            if m:
                key = m.groupdict()["key"]
                kvs = {key: []}
                self.entry[ENTRY_DATA_KEY].append(kvs)

                return None

            m = self.match("multilines_data", line)
            if m:
                d = self.entry[ENTRY_DATA_KEY][-1]  # Last ml data :: dict
                key = [k for k, _vs in SC.iteritems(d)][0]
                v_add = m.groupdict()["value"]
                vs = self.entry[ENTRY_DATA_KEY][-1][key]

                # It seems there are some special cases like:
                #
                #    Installable Languages: 1
                #        en|US|iso8859-1
                #
                if not isinstance(vs, list):
                    self.entry[ENTRY_DATA_KEY][-1][key] = [vs]

                print "key=%s, vs=%s, v_add=%s" % (key, str(vs), v_add)
                self.entry[ENTRY_DATA_KEY][-1][key].append(v_add)

        return None

# vim:sw=4:ts=4:et:
