#
# Copyright (C) 2013 Red Hat, Inc.
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.scanner.runlevel as TT
import sos_analyzer.tests.common as C
import anyconfig
import os.path
import os
import re
import unittest


MATCHED_EXAMPLES = ["unknown", "N 3", "5 3"]
NOT_MATCHED_EXAMPLES = ['', "# comment", "Invalid pattern", "10"]


def make_workdir_and_scanners(scls=TT.Scanner, examples=MATCHED_EXAMPLES):
    workdir = C.setup_workdir()
    yield workdir

    is_new_scanner_cls = getattr(scls, "inputs", False)

    # pylint: disable=maybe-no-member
    for i, v in enumerate(MATCHED_EXAMPLES):
        datadir = os.path.join(workdir, "data_%d" % i)
        f = os.path.join(datadir, (scls.inputs if is_new_scanner_cls else
                                   scls.input_name))
        os.makedirs(os.path.dirname(f))
        open(f, 'w').write(v + "\n")

        if is_new_scanner_cls:
            yield scls(datadir, os.path.join(workdir,
                                             scls.outputs_dir + "_%d" % i))
        else:
            yield scls(workdir, datadir)
    # pylint: enable=maybe-no-member


class Test_00_pure_functions(unittest.TestCase):

    def test_00_regexp(self):
        for s in MATCHED_EXAMPLES:
            self.assertTrue(re.match(TT.MATCH_RE, s))


class Test_10_Scanner(unittest.TestCase):

    def setUp(self):
        ts = list(make_workdir_and_scanners())
        (self.workdir, self.scanners) = (ts[0], ts[1:])

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_20_scan_file(self):
        for sc in self.scanners:
            self.assertTrue(sc.scan_file())

    def test_30_run(self):
        for sc in self.scanners:
            sc.run()
            self.assertTrue(sc.result)
            self.assertTrue(os.path.exists(sc.output_path))
            self.assertTrue(sc.result.get("data", None))


class Test_20_Scanner2(unittest.TestCase):

    def setUp(self):
        ts = list(make_workdir_and_scanners(TT.Scanner2))
        (self.workdir, self.scanners) = (ts[0], ts[1:])

    def tearDown(self):
        C.cleanup_workdir(self.workdir)

    def test_10_get_pattern(self):
        for sc in self.scanners:
            self.assertTrue(sc.get_pattern("match_patterns", False))

    def test_20_process_line(self):
        for sc in self.scanners:
            for s in NOT_MATCHED_EXAMPLES:
                self.assertFalse(sc.process_line(s), s)

            for s in MATCHED_EXAMPLES:
                self.assertTrue(sc.process_line(s), s)

    def test_40_run(self):
        for sc in self.scanners:
            sc.run()

            # pylint: disable=maybe-no-member
            outfile = sc._mk_output_path(sc.inputs)
            # print >> open("/tmp/t.log", 'a'), "outfile=" + outfile
            self.assertTrue(os.path.exists(outfile))

            x = anyconfig.load(outfile)
            self.assertTrue(x.get("data", None), str(x))
            # pylint: enable=maybe-no-member

# vim:sw=4:ts=4:et:
