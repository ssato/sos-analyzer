#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.scanner.base as SSB
import re


"""/etc/fstab formats:
1:
LABEL=/                 /                       ext3    defaults        1 1
LABEL=/home             /home                   ext3    defaults        1 2
LABEL=/var              /var                    ext3    defaults        1 2
LABEL=/var/crash        /var/crash              ext3    defaults        1 2
LABEL=/opt              /opt                    ext3    defaults        1 2
LABEL=/tmp              /tmp                    ext3    defaults        1 2
LABEL=/boot             /boot                   ext3    defaults        1 2
tmpfs                   /dev/shm                tmpfs   defaults        0 0
devpts                  /dev/pts                devpts  gid=5,mode=620  0 0
sysfs                   /sys                    sysfs   defaults        0 0
proc                    /proc                   proc    defaults        0 0
LABEL=SWAP              swap                    swap    defaults        0 0
192.168.122.1:/exports/contents   /contents   nfs soft,tcp 0 0

2:

# /etc/fstab
# Created by anaconda on Thu Sep  6 03:18:30 2012
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
/dev/mapper/vg0-lv_root /                       ext4    defaults,discard        1 1
UUID=da3f02a9-7efc-4aef-a1cb-52dc5d05daec /boot                   ext4    defaults,discard        1 2
/dev/mapper/luks-2db91808-6024-4596-be79-d5870ed4e8f2 /home                   ext4    defaults,discard        1 2
/dev/mapper/vg0-lv_swap swap                    swap    defaults        0 0
#
#/run/media/ssato/c8d37830-3006-4a16-9f2c-98f50d370075/images /var/lib/libvirt/images/bases     none    rw,bind,noauto 0 0
mtpfs   /media/galaxy_nexus     fuse.mtpfs    allow_other,rw,user,noauto        0 0
/var/lib/repos/ssato    /home/ssato/repos/public/       none    bind    0 0
"""

FS_RE = r"^(?P<device>\S+)\s+(?P<mount_point>\S+)\s+(?P<filesystem>\S+)" + \
        r"\s+(?P<options>\S+)(?:\s+(?P<dump>\d)\s+(?P<fsck>\d))?$"


class Scanner(SSB.SinglePatternScanner):

    name = input_name = "etc/fstab"
    ignore_pattern = r"^(?:^#.*|\s*)$"
    pattern = FS_RE

# vim:sw=4:ts=4:et:
