#
# Base classes for runnable classes such like scanners and analyzers.
#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.compat as SC
import sos_analyzer.utils as SU
import glob
import os.path
import os


DICT_MZERO = dict()
_ERR_NOT_IMPL = "Child class must implement this!"


class Runnable(object):

    name = "runnable"
    version = "0.0.1"
    enabled = True

    def __init__(self, name=None, **kwargs):
        """
        :param name: Object's name
        """
        if name is not None:
            self.name = name

        for k, v in SC.iteritems(kwargs):
            if v is not None:
                setattr(self, k, v)

    def run(self):
        raise NotImplementedError(_ERR_NOT_IMPL)


class RunnableWithConfig(Runnable):

    conf = DICT_MZERO

    def __init__(self, name=None, conf=None, **kwargs):
        """
        :param name: Object's name
        :param conf: A maybe nested dict holding object's configurations
        """
        super(RunnableWithConfig, self).__init__(name, **kwargs)

        if conf is not None and isinstance(conf, dict):
            self.conf = conf.get(self.name, DICT_MZERO)

        if self.getconf("disabled", False) or not self.getconf("enabled",
                                                               True):
            self.enabled = False

    def getconf(self, key, fallback=None, key_sep='.'):
        """
        :param key: Key to get configuration
        :param fallback: Fallback value if the value for given key is not found
        :param key_sep: Separator char to represents hierarchized configuraion
        """
        return SU.dic_get_recur(self.conf, key, fallback, key_sep)


class RunnableWithIO(RunnableWithConfig):

    inputs_dir = os.path.sep  # '/' (root)
    inputs = []
    outputs_dir = os.curdir
    glob_pattern = '*'

    def __init__(self, inputs_dir=None, outputs_dir=None, inputs=None,
                 name=None, conf=None, **kwargs):
        """
        :param inputs_dir: Path to dir holding inputs
        :param outputs_dir: Path to dir to save results
        :param inputs: List of filenames, path to input files, glob pattern
            of filename or None; ex. ["a/b.txt", "c.txt"], "a/b/*.yml"
        :param name: Object's name
        :param conf: A maybe nested dict holding object's configurations
        """
        super(RunnableWithIO, self).__init__(name, conf, inputs_dir=inputs_dir,
                                             outputs_dir=outputs_dir,
                                             inputs=inputs, **kwargs)
        if isinstance(self.inputs, list):
            self.input_paths = [(inp, self._mk_input_path(inp)) for inp
                                in self.inputs]
        else:
            ips = glob.glob(self._mk_input_path(self.inputs))  # Effectful.
            idir = os.path.dirname(self.inputs)
            self.input_paths = [(os.path.join(idir, os.path.basename(inp)),
                                 inp) for inp in ips]

    def _mk_input_path(self, input):
        """
        :param input: Input filename or path to input file
        :return: Path to output file
        """
        return os.path.join(self.inputs_dir, input)

    def _mk_output_path(self, input, ext=".json"):
        """
        NOTE: Child class should override this method.

        :param input: Input filename or path to input file
        :return: Path to output file
        """
        return os.path.join(self.outputs_dir, input + ext)

    def process_line(self, line, i):
        return dict(lineno=i, line=line)

    def process_input_impl(self, fileobj):
        for i, line in enumerate(fileobj.readlines()):
            line = line.rstrip()
            if line:
                yield self.process_line(line, i)

    def process_input(self, input_path):
        """
        :param input_path: Input file path
        :return: A list of results or []
        """
        try:
            f = open(input_path)
            return [x for x in self.process_input_impl(f) if x]

        except (IOError, OSError) as e:
            logging.warn("Could not open the input: " + input_path)
            return []

    def process_inputs(self, *args, **kwargs):
        for relpath, path in self.input_paths:
            result = dict(name=self.name, version=self.version,
                          data=self.process_input(path))
            outpath = self._mk_output_path(relpath)

            d = os.path.dirname(outpath)
            if not os.path.exists(d):
                os.makedirs(d)

            SC.json.dump(result, open(outpath, 'w'))

    def run(self):
        self.process_inputs()

# vim:sw=4:ts=4:et:
