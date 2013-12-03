#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging
import pkg_resources


SCANNERS = []

for e in pkg_resources.iter_entry_points("sos_analyzer_scanners"):
    try:
        SCANNERS.append(e.load())
    except ImportError:
        logging.warn("Could not load and append: " + str(e))
        continue

# vim:sw=4:ts=4:et:
