#
# Copyright (C) 2013 - 2015 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
"""rpm -Va output format (verify options in rpm(8)):
....L....  c /etc/pam.d/smartcard-auth
....L....  c /etc/pam.d/system-auth
S.5....T.    /usr/lib/python2.6/site-packages/jinja2_cli/render.py
S.5....T.    /usr/lib/python2.6/site-packages/jinja2_cli/render.pyc
prelink: /usr/lib64/libyajl.so.1.0.7: at least one of file's dependencies \
    has changed since prelinking
S.?......    /usr/lib64/libyajl.so.1.0.7

# Verification result fields:

S file Size differs
M Mode differs (includes permissions and file type)
5 digest (formerly MD5 sum) differs
D Device major/minor number mismatch
L readLink(2) path mismatch
U User ownership differs
G Group ownership differs
T mTime differs
P caPabilities differ
"""
import sos_analyzer.scanner.base


PRELINK_RE = r"^prelink: (?P<path>[^:\s]+): .*$"
MODIFIED_RE = r"^(?P<size>[S.?])(?P<mode>[M.?])(?P<checksum>[5.?])" + \
              r"(?P<device>[D.?])(?P<readlink_path>[L.?])" + \
              r"(?P<user>[U.?])(?P<group>[G.?])(?P<mtime>[T.?])" + \
              r"(?P<capabilities>[P.?])\s+(?P<attr>[cdglr.])?\s*" + \
              r"(?P<path>\S+)$"
OTHER_RE = r"^\s+(?P<error>.*)\s*$"  # Error messages, etc.


class Scanner(sos_analyzer.scanner.base.MultiPatternsScanner):

    name = input_name = "rpm-Va"
    multi_patterns = (PRELINK_RE, MODIFIED_RE, OTHER_RE)

# vim:sw=4:ts=4:et:
