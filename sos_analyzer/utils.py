#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from logging import WARN, INFO, DEBUG

import glob
import logging
import os.path
import tempfile


LOGGER = logging.getLogger(__name__)


def to_log_level(level):
    assert level >= 0 and level < 3, "wrong log level passed: " + str(level)
    return [WARN, INFO, DEBUG][level]


def set_loglevel(level):
    """
    :param level: Log level = 0, 1, 2
    """
    LOGGER.getLogger().setLevel(to_log_level(level))


def find_dir_has_target(topdir, target):
    """
    Find the path to dir under given ``topdir`` which has ``taget``.

    :param topdir: Top dir to traverse to find target
    :param target: Target file or dir to find
    :return: Path to the objective dir
    """
    if os.path.exists(os.path.join(topdir, target)):
        return topdir

    subdirs = [x for x in glob.glob(os.path.join(topdir, '*'))
               if os.path.isdir(x)]

    for d in subdirs:
        x = find_dir_has_target(d, target)
        if x:
            return x

    LOGGER.debug("Given dir does not look having target: %s", topdir)
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
                LOGGER.info("Working dir already exists: %s", workdir)
                return workdir
            else:
                m = "Given working dir is not a dir: " + workdir
                raise RuntimeError(m)
        else:
            os.makedirs(workdir)
            return workdir


def dic_get_recur(dic, key, fallback=None, key_sep='.'):
    """
    Recursively traverse maybe nested dicts and return the value.

    :param key: Key string :: str, ustr
    :param fallback: Fallback value if key not found in dic
    :param dic: Target dict object
    :param key_sep: Key separator

    >>> dic_get_recur({}, "a.b.c") is None
    True
    >>> dic_get_recur(dict(a=1, ), "b") is None
    True
    >>> dic_get_recur(dict(a=1, ), "a")
    1
    >>> dic_get_recur(dict(a=dict(b=dict(c=1, ), ), ), "a.b.c")
    1
    """
    assert isinstance(dic, dict), \
        "First argument 'dic' is not a dict instance: " + str(dic)
    assert isinstance(key, str) or isinstance(key, unicode), \
        "Second argument 'key' is not a string object: " + str(key)

    if key_sep in key:
        key_0 = key[:key.find(key_sep)]
        if key_0 not in dic:
            return fallback

        new_dic = dic[key[:key.find(key_sep)]]

        if not isinstance(new_dic, dict):
            return fallback

        new_key = key[key.find(key_sep) + 1:]
        return dic_get_recur(new_dic, new_key, fallback, key_sep)
    else:
        return dic.get(key, fallback)

# vim:sw=4:ts=4:et:
