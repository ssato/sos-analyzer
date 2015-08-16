#
# Copyright (C) 2013 - 2015 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
"""/etc/kdump.conf format:

# See the kdump.conf(5) man page for details of configuration directives
#raw /dev/sda5
#ext3 /dev/sda3
#ext3 LABEL=/boot
#ext3 UUID=03138356-5e61-4ab3-b58e-27507ac41937
#net my.server.com:/export/tmp
#net user@my.server.com
#path /var/crash
#core_collector makedumpfile -c --message-level 1
#core_collector cp --sparse=always
#link_delay 60
#kdump_post /var/crash/scripts/kdump-post.sh
#extra_bins /usr/bin/lftp
#disk_timeout 30
#extra_modules gfs2
#options modulename options
#default shell
"""
import sos_analyzer.scanner.base


# kdump save location options:
#  raw <partition> | net (<nfs mount> | <user@server>) | path <path> |
#  <fs_type> <partition>
#    where fs_type = ext4 | ext3 | ext2 | minix | xfs

SAVE_LOCATION_RE = (r"^(?P<save_option>(?:"
                    r"(?:raw|ext4|ext3|ext2|minix|xfs)\s+(?P<partition>\S+)|"
                    r"net\s+(?P<remote_dest>\S+)|"
                    r"path\s+(?P<path>\S+)))$")
OTHER_RE = r"^(?P<option>[^#].*)$"


class Scanner(sos_analyzer.scanner.base.MultiPatternsScanner):

    name = input_name = "etc/kdump.conf"
    multi_patterns = (SAVE_LOCATION_RE, OTHER_RE)  # @see kdump.conf(5)

# vim:sw=4:ts=4:et:
