#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.analyzer.base as Base
import sos_analyzer.compat as SC
import os.path
import re


def get_cur_runlevel(workdir, default=3,
                     input="sos_commands/startup/runlevel.json"):
    """
    :see: ``sos_analyzer.scanner.runlevel``
    """
    data = Base.load_scanned_data(workdir, input)
    if data:
        return int(data[0].get("cur_runlevel", default))

    return default


def is_sshd_enabled(workdir, runlevel=3, input="chkconfig.json"):
    """
    :see: ``sos_analyzer.scanner.chkconfig``
    """
    data = Base.load_scanned_data(workdir, input)
    if not data:
        return None

    sshd_enabled = False
    runlevel = get_cur_runlevel(workdir, runlevel)

    for d in data:
        if d.get("service", None) == "sshd":
            sshd_enabled = d.get("status", [])[runlevel] == "on"
            break

    return sshd_enabled


def is_root_login_enabled(workdir, runlevel=3,
                          input="etc/ssh/sshd_config.json"):
    """
    :see: ``sos_analyzer.scanner.etc_ssh_sshd_config``
    """
    data = Base.load_scanned_data(workdir, input)
    if not data:
        return None

    for d in data:
        if d.get("config", None) == "PermitRootLogin":
            if d.get("value", None) == "yes":
                return True

    return False


class Analyzer(Base.Analyzer):

    name = "ssh"

    def analyze(self, *args, **kwargs):
        return dict(is_sshd_enabled=is_sshd_enabled(self.workdir),
                    is_root_login_enabled=is_root_login_enabled(self.workdir))

# vim:sw=4:ts=4:et:
