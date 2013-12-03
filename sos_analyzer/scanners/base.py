#
# Base class for scanners.
#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging, \
    SCANNER_RESULTS_SUBDIR as SUBDIR

import sos_analyzer.compat as SC
import os.path
import re


NULL_DICT = dict()


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
    if key_sep in key:
        key_0 = key[:key.find(key_sep)]
        if key_0 not in dic:
            return fallback

        new_dic = dic[key[:key.find(key_sep)]]
        new_key = key[key.find(key_sep) + 1:]
        return dic_get_recur(new_dic, new_key, fallback, key_sep)
    else:
        return dic.get(key, fallback)


def compile_patterns(conf={}):
    """
    >>> cps = compile_patterns(dict(patterns=dict(aaa=r"([a-z]+)",
    ...                                           bbb=r"([0-9]+)")))
    >>> assert cps["aaa"].match("abc") is not None
    >>> assert cps["bbb"].match("123") is not None
    """
    return dict((k, re.compile(v)) for k, v in
                SC.iteritems(conf.get("patterns", NULL_DICT)))


class BaseScanner(object):

    name = "base"
    input_name = "base"
    conf = NULL_DICT

    def __init__(self, workdir, datadir, input_name=None, name=None,
                 conf=None, subdir=SUBDIR):
        """
        """
        self.datadir = datadir

        if input_name is not None:
            self.input_name = input_name

        if name is not None:
            self.name = name

        if conf is not None and isinstance(conf, dict):
            self.conf = conf

        self.input_path = os.path.join(datadir, self.input_name)
        self.patterns = compile_patterns(self.conf)
        self.output_path = os.path.join(workdir, subdir, "%s.json" % self.name)

    def getconf(self, key, fallback=None, key_sep='.'):
        return dic_get_recur(self.conf, key, fallback, key_sep)

    def match(self, name, s):
        return self.patterns.get(name, re.compile(r".*")).match(s)

    def _update_state(self, state, line, i):
        """
        :param state: A string or int represents the current state
        :param line: Content of the line
        :param i: Line number in the input file
        """
        return state

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        return dict()

    def parse(self, content):
        """
        Parse the content of input file.

        :param content: Content of the input file.
        """
        state = self.getconf("initial_state", 0)

        for i, line in enumerate(content.splitlines()):
            line = line.rstrip()

            if not line and self.getconf("ignore_empty_lines", True):
                continue

            new_state = self._update_state(state, line, i)
            if state != new_state:
                logging.info("State changed: %d -> %d" % (state, new_state))
                state = new_state

            yield self.parse_impl(state, line, i)

    def scan_file(self):
        """
        Scan the input file and return parsed result.
        """
        try:
            f = open(self.input_path)
            c = f.read()

            if not c:
                logging.warn("Empty file: " + self.input_path)
                return []

            return [x for x in self.parse(c) if x]

        except (IOError, OSError) as e:
            logging.warn("Could not open the input: " + self.input_path)
            return []

    def run(self):
        self.result = dict(data=self.scan_file())
        SC.json.dump(self.result, open(self.output_path, 'w'))

# vim:sw=4:ts=4:et:
