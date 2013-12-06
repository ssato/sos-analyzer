#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.analyzer.base as Base
import sos_analyzer.compat as SC
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
        logging.warn("Could not find the default boot idx" + f)
        return None

    default_boot_version = None
    kernels = [d for d in data if d.get("title", False)]
    try:
        return kernels[default_boot_idx].get("kernel", None)
    except Exception as e:
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

        return dict(running_kernel=k1,
                    default_boot_kernel=k2,
                    installed_kernels=iks,
                    is_latest_kernel_running=(iks[-1] == k1))

# vim:sw=4:ts=4:et:
