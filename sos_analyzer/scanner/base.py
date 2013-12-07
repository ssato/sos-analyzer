#
# Base class for scanners.
#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
from sos_analyzer.globals import LOGGER as logging, scanned_datadir

import sos_analyzer.compat as SC
import sos_analyzer.utils as SU
import glob
import os
import os.path
import re


DICT_MZERO = dict()


def compile_patterns(conf={}):
    """
    >>> cps = compile_patterns(dict(patterns=dict(aaa=r"([a-z]+)",
    ...                                           bbb=r"([0-9]+)")))
    >>> assert cps["aaa"].match("abc") is not None
    >>> assert cps["bbb"].match("123") is not None
    """
    return dict((k, re.compile(v)) for k, v in
                SC.iteritems(conf.get("patterns", DICT_MZERO)))


class BaseScanner(object):

    name = "base"
    input_name = "base"
    conf = DICT_MZERO
    initial_state = "initial_state"

    def __init__(self, workdir, datadir, input_name=None, name=None,
                 conf=None, **kwargs):
        """
        :param workdir: Working dir to save results
        :param datadir: Data dir where input data file exists
        :param input_name: Input file name
        :param name: Scanner's name
        :param conf: A dict object holding scanner's configurations
        """
        self.datadir = datadir

        if input_name is not None:
            self.input_name = input_name

        if name is not None:
            self.name = name

        if conf is not None and isinstance(conf, dict):
            self.conf = conf.get(self.name, DICT_MZERO)

        if self.getconf("disabled", False) or \
           not self.getconf("enabled", True):
            self.enabled = False
        else:
            self.enabled = True

        self.input_path = os.path.join(datadir, self.input_name)
        self.patterns = compile_patterns(self.conf)
        self.output_path = os.path.join(scanned_datadir(workdir),
                                        "%s.json" % self.name)

    def getconf(self, key, fallback=None, key_sep='.'):
        """
        :param key: Key to get configuration
        :param fallback: Fallback value if the value for given key is not found
        :param key_sep: Separator char to represents hierarchized configuraion
        """
        return SU.dic_get_recur(self.conf, key, fallback, key_sep)

    def match(self, name, s):
        """
        :param name: Regex pattern's name
        :param s: Target string to try to match with
        """
        return self.patterns.get(name, re.compile(r".*")).match(s)

    def _update_state(self, state, line, i):
        """
        Update the internal state.

        :param state: A string or int represents the current state
        :param line: Content of the line
        :param i: Line number in the input file
        """
        return state

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        parser implementation.

        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        return dict()

    def parse(self, fileobj):
        """
        Parse the content of input file.

        :param fileobj: Input file object.
        """
        state = self.getconf("initial_state", self.initial_state)

        for i, line in enumerate(fileobj.readlines()):
            line = line.rstrip()

            if not line and self.getconf("ignore_empty_lines", True):
                continue

            new_state = self._update_state(state, line, i)
            if state != new_state:
                m = "State changed: %s -> %s, line=%s" % \
                    (str(state), str(new_state), line)
                logging.debug(m)
                state = new_state

            yield self.parse_impl(state, line, i)

    def scan_file(self):
        """
        Scan the input file and return parsed result.
        """
        try:
            f = open(self.input_path)
            return [x for x in self.parse(f) if x]

        except (IOError, OSError) as e:
            logging.warn("Could not open the input: " + self.input_path)
            return []

    def run(self):
        self.result = dict(data=self.scan_file())

        d = os.path.dirname(self.output_path)
        if not os.path.exists(d):
            os.makedirs(d)

        SC.json.dump(self.result, open(self.output_path, 'w'))


class SinglePatternScanner(BaseScanner):

    pattern = r"^.*$"
    ignore_pattern = r"^#.*$"

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        if re.match(self.ignore_pattern, line):
            return None

        m = re.match(self.pattern, line)
        if m:
            return m.groupdict()
        else:
            e = "Invalid input? file=%s, line=%s" % (self.input_path, line)
            logging.warn(e)
            return None


class MultiPatternsScanner(SinglePatternScanner):

    multi_patterns = []

    def parse_impl(self, state, line, i, *args, **kwargs):
        """
        :param state: A dict object represents internal state
        :param line: Content of the line
        :param i: Line number in the input file
        :return: A dict instance of parsed result
        """
        if re.match(self.ignore_pattern, line):
            return None

        for pattern in self.multi_patterns:
            logging.debug("Try the pattern: " + pattern)
            m = re.match(pattern, line)
            if m:
                return m.groupdict()

        m = "No patterns matched: file=%s, line=%s" % (self.input_path, line)
        logging.warn(m)

        return None


class MultiInputsScanner(BaseScanner):

    name = "multiinput"
    input_names = "*"  # or [] ?
    conf = DICT_MZERO

    def __init__(self, workdir, datadir, input_names=None, name=None,
                 conf=None):
        """
        :param workdir: Working dir to save results
        :param datadir: Data dir where input data file exists
        :param input_names: List of input file names or its glob pattern
        :param name: Scanner's name
        :param conf: A dict object holding scanner's configurations
        """
        self.datadir = datadir

        if input_names is not None:
            self.input_names = input_names

        if name is not None:
            self.name = name

        if conf is not None and isinstance(conf, dict):
            self.conf = conf.get(self.name, DICT_MZERO)

        if self.getconf("disabled", False) or \
           not self.getconf("enabled", True):
            self.enabled = False
        else:
            self.enabled = True

        if isinstance(self.input_names, list):
            self.input_paths = [os.path.join(datadir, n) for n
                                in self.input_names]
        else:
            self.input_paths = glob.glob(os.path.join(datadir,
                                                      self.input_names))

        self.patterns = compile_patterns(self.conf)
        self.output_path = os.path.join(scanned_datadir(workdir),
                                        "%s.json" % self.name)

    def scan_files_g(self):
        """
        Scan the input files and return parsed result.
        """
        for input_path in self.input_paths:
            try:
                f = open(input_path)
                yield (input_path, [x for x in self.parse(f) if x])

            except (IOError, OSError) as e:
                logging.warn("Could not open the input: " + input_path)
                yield (input_path, [])

    def scan_files(self):
        return [dict(path=t[0], data=t[1]) for t in self.scan_files_g()]

    def run(self):
        self.result = dict(data=self.scan_files())

        d = os.path.dirname(self.output_path)
        if not os.path.exists(d):
            os.makedirs(d)

        SC.json.dump(self.result, open(self.output_path, 'w'))

# vim:sw=4:ts=4:et:
