#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.analyzer.base as Base
import sos_analyzer.analyzer.filesystem as SAF
import os.path
import re


def get_kernel_version_from_uname(workdir, input="uname.json"):
    """
    :see: ``sos_analyzer.scanner.uname``
    """
    data = Base.load_scanned_data(workdir, input)
    if data:
        return data[0].get("kernel_release", None)

    return None


def get_kernel_version_from_grub_conf(workdir,
                                      input="boot/grub/grub.conf.json"):
    """
    :see: ``sos_analyzer.scanner.grub``
    """
    data = Base.load_scanned_data(workdir, input)
    if not data:
        return None

    default_boot_idx = None
    for d in data:
        if d.get("option", None) == "default":
            default_boot_idx = int(d.get("value", 0))
            break

    if default_boot_idx is None:
        logging.warn("Could not find the default boot idx in " + input)
        return None

    kernels = [d for d in data if d.get("title", False)]
    try:
        return kernels[default_boot_idx].get("kernel", None)
    except Exception:
        logging.error("Failed to get the default boot kernel")
        return None


KERNEL_RE = re.compile(r"^kernel-(\d\S+)\.[^.]+$")


def list_installed_kernels(workdir, input="installed-rpms.json"):
    """
    :see: ``sos_analyzer.scanner.installed_rpms``
    """
    data = Base.load_scanned_data(workdir, input)
    if not data:
        return None

    def pick_kernels(data):
        for d in data:
            rpm = d.get("rpm", None)
            if not rpm.startswith("kernel-"):
                continue

            m = KERNEL_RE.match(rpm)
            if m:
                yield m.groups()[0]

    # TODO: Check this works (ordered from the later ones).
    return sorted(pick_kernels(data), reverse=True)


def path_patterns(path):
    """
    >>> path_patterns("/a/b/c/d/e")
    ['/a/b/c/d/e', '/a/b/c/d', '/a/b/c', '/a/b', '/a', '/']
    """
    ps = path.split(os.path.sep)
    pss = [os.path.join(os.path.sep, *ps[:i][1:]) for i
           in range(1, len(ps) + 1)]
    return list(reversed(pss))


def find_kdump_partition(workdir, input="etc/kdump.conf.json"):
    """
    FIXME: Implement the logic to check kdump partition is large enough.

    :see: ``sos_analyzer.scanner.etc_kdump_conf``
    """
    data = Base.load_scanned_data(workdir, input)
    if not data:
        return None

    path = "/var/crash"  # @see kdump.conf(5)
    partition = None

    for d in data:
        if d.get("path", False):
            path = d["path"]  # noqa: not implemented yet.
        if d.get("partition", False):
            partition = d["partition"]

    if partition:   # e.g. /dev/sda3, LABEL=/boot, UUID=...
        fss = SAF.list_normal_filesystems(workdir)  # noqa: likewise.

        pass


def is_sysrq_enabled(workdir, input="sos_commands/kernel/sysctl_-a.json"):
    """
    :see: ``sos_analyzer.scanner.sysctl_a``
    """
    data = Base.load_scanned_data(workdir, input)
    if not data:
        return None

    for d in data:
        if d["parameter"] == "kernel.sysrq":
            return d.get("value", '0') == '1'

    return False


class Analyzer(Base.Analyzer):

    name = "kernel"
    inputs = []

    # TODO: Make them automatically loaded and these data referable.
    scanned_inputs = ["boot/grub/grub.conf.json",
                      "uname.json"]

    def analyze(self, *args, **kwargs):
        k1 = get_kernel_version_from_uname(self.workdir)
        k2 = get_kernel_version_from_grub_conf(self.workdir)
        iks = list_installed_kernels(self.workdir)
        sysrq_enabled = is_sysrq_enabled(self.workdir)

        return dict(running_kernel=k1,
                    default_boot_kernel=k2,
                    installed_kernels=iks,
                    is_latest_kernel_running=(iks[-1] == k1),
                    sysrq_enabled=sysrq_enabled)

# vim:sw=4:ts=4:et:
