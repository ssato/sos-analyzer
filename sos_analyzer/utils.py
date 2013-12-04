#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from logging import WARN, INFO, DEBUG
from sos_analyzer.globals import LOGGER as logging

import glob
import os.path
import tempfile


def to_log_level(level):
    assert level >= 0 and level < 3, "wrong log level passed: " + str(level)
    return [WARN, INFO, DEBUG][level]


def set_loglevel(level):
    """
    :param level: Log level = 0, 1, 2
    """
    logging.setLevel(to_log_level(level))


def find_dir_having_target(topdir, target):
    """
    Find the path to dir having ``taget`` under given dir ``topdir``.

    :param topdir: Top dir to traverse to find target
    :param target: Target file or dir to find
    :return: Path to the objective dir
    """
    if os.path.exists(os.path.join(topdir, target)):
        return topdir

    subdirs = [x for x in glob.glob(os.path.join(topdir, '*'))
               if os.path.isdir(x)]

    for d in subdirs:
        x = find_dir_having_target(d, target)
        if x:
            return x

    logging.debug("Given dir does not look having target: " + topdir)
    return None


def setup_workdir(workdir=None):
    """
    Setup working dir to save results.

    :param workdir: Dir path or None. Create an unique dir if None was given.
    """
    if workdir is None:
        return tempfile.mkdtemp(dir="/tmp", prefix="sos_analyzer-")
    else:
        if os.path.exists(workdir):
            if os.path.isdir(workdir):
                logging.info("Working dir already exists: " + workdir)
                return workdir
            else:
                m = "Given working dir is not a dir: " + workdir
                raise RuntimeError(m)
        else:
            os.makedirs(workdir)
            return workdir

# vim:sw=4:ts=4:et:
