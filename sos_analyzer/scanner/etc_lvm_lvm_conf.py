#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import sos_analyzer.compat as SC


""" /etc/lvm/lvm.conf format:

From 'syntax' section in lvm.conf(5):

       file = value*
              A configuration file consists of a set of values.

       value = section | assignment
              A value can either be a new section, or an assignment.

       section = identifier '{' value* '}'
              A section is groups associated values together.
              It is denoted by a name and delimited by curly brackets.
              e.g. backup {
                        ...
                   }

       assignment = identifier '=' ( array | type )
              An assignment associates a type with an identifier.
              e.g. max_archives = 42

       array =  '[' ( type ',')* type ']' | '[' ']'
              Inhomogeneous arrays are supported.
              Elements must be separated by commas.
              An empty array is acceptable.

       type = integer | float | string
              integer = [0-9]*
              float = [0-9]*'.'[0-9]*
              string = '"'.*'"'

              Strings must be enclosed in double quotes.
"""

STATES = (IN_SECTION, BEGIN_SECTION, END_SECTION, AT_ASSIGNMENT_LINE) = \
         ("in_section", "begin_section", "end_section", "at_assignment_line")

ASSIGN_RE = r"\s*(?P<key>\S+)\s*=\s*(?P<value>.*)\s*"

CONF = dict(initial_state=END_SECTION,
            ignore_empty_lines=1,
            patterns=dict(begin_section=r"(\S+)\s+{.*",
                          end_section=r"^\s*}.*$",
                          assignment=ASSIGN_RE))


def kvs_to_a_dict(kvs):
    k = kvs["key"]
    v = kvs["value"]
    return {k: v}


class Scanner(SSB.BaseScanner):

    name = input_name = "etc/lvm/lvm.conf"
    conf = CONF
    initial_state = END_SECTION
    section = {}  # Hold space.

    def _update_state(self, state, line, i):
        """
        Update the internal state.

        :param state: A string or int represents the current state
        :param line: Content of the line
        :param i: Line number in the input file
        """
        if self.match("begin_section", line):
            return BEGIN_SECTION

        if self.match("end_section", line):
            return END_SECTION

        if state == BEGIN_SECTION:
            return IN_SECTION  # Next state
        else:
            return state  # No change

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        if state == END_SECTION:
            return self.section

        if state == IN_SECTION:
            m = self.match("assignment", line)
            if m:
                kv = m.groupdict()
                vs = self.section.get("values", {})
                vs[kv["key"]] = eval(kv["value"])
                self.section["values"] = vs
            else:
                #e = "Not a line of assignment? l=%s, lno=%d" % (line, i)
                #logging.warn(e)
                pass

        elif state == BEGIN_SECTION:
            m = self.match("begin_section", line)
            if m:
                t = m.groups()
                self.section = dict(title=t[0], )
        else:
            pass

        return None

# vim:sw=4:ts=4:et:
