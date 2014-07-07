#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.analyzer.base as Base


LOCALE_RE = r"^(?P<locale>[^.]+.(?P<charset>\S+))$"


def get_locale(workdir, input="etc/sysconfig/i18n.json"):
    """
    :see: ``sos_analyzer.scanner.etc_sysconfig_i18n``
    """
    data = Base.load_scanned_data(workdir, input)
    if data:
        for d in data:
            if d.get("option", '') == "LANG":
                return d.get("value")


class Analyzer(Base.Analyzer):

    name = "i18n"

    def analyze(self, *args, **kwargs):
        loc = get_locale(self.workdir)
        iulu = loc.endswith(".UTF-8")

        return dict(is_unsupported_locale_used=iulu, )

# vim:sw=4:ts=4:et:
