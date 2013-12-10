#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging

import sos_analyzer.analyzer.base as Base
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


def _is_fully_disabled(svc):
    return "service" in svc and all("off" == st for st
                                    in svc.get("status", []))


def list_services_on_cur_runlevel(workdir, runlevel=3, input="chkconfig.json"):
    """
    :see: ``sos_analyzer.scanner.chkconfig``
    """
    data = Base.load_scanned_data(workdir, input)
    if not data:
        return None

    runlevel = get_cur_runlevel(workdir, runlevel)

    enabled_svcs = [s["service"] for s in data
                    if "service" in s and s["status"][runlevel] == "on"]

    disabled_svcs = [s["service"] for s in data
                     if "service" in s and s["status"][runlevel] == "off"]
    fully_disabled_svcs = [s["service"] for s in data if _is_fully_disabled(s)]

    enabled_xinetd_svcs = [s["xinetd_service"] for s in data
                           if s["status"] == "on"]

    return dict(enabled_services=enabled_svcs,
                disabled_services=disabled_svcs,
                fully_disabled_services=fully_disabled_svcs,
                enabled_xinetd_services=enabled_xinetd_svcs)


def is_service_enabled(svcs, svcname, or_op='|'):
    ss = svcname.split(or_op) if or_op in svcname else [svcname]
    for s in ss:
        if s in svcs["enabled_services"]:
            return True

    return False


class Analyzer(Base.Analyzer):

    name = "services"
    important_services = ["sshd", "ntpd", "syslog|rsyslog", "sysstat"]
    not_secure_services = ["telnet", "rexec", "rlogin", "rsh"]

    def analyze(self, *args, **kwargs):
        ret = dict()
        svcs = list_services_on_cur_runlevel(self.workdir)

        for isvc in self.getconf("important_services",
                                 self.important_services):
            ret["is_%s_enabled" % isvc] = is_service_enabled(svcs, isvc)

        ret["unsecure_xinetd_services_enabled"] = \
            [s for s in svcs["enabled_xinetd_services"]
             if s in self.getconf("not_secure_services",
                                  self.not_secure_services)]

        ss = svcs["fully_disabled_services"]
        ret["fully_disabled_services"] = ss
        ret["number_of_fully_disabled_services"] = len(ss)

        return ret

# vim:sw=4:ts=4:et:
