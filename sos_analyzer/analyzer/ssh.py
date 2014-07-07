#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.analyzer.base as Base
import sos_analyzer.analyzer.system_service as SAS


def is_sshd_enabled(workdir, runlevel=3):
    """
    :see: ``sos_analyzer.analyzer.system_service``
    """
    svcs = SAS.list_services_on_cur_runlevel(workdir, runlevel)
    return SAS.is_service_enabled(svcs, "sshd")


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
