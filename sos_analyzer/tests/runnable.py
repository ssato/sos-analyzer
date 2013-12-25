#
# Copyright (C) 2013 Satoru SATOH <ssato @ redhat.com>
# License: GPLv3+
#
import sos_analyzer.runnable as TT
import os.path
import random
import unittest


class Test_00_Runnable(unittest.TestCase):

    def test_00__init__w_no_args(self):
        r = TT.Runnable()

        self.assertTrue(isinstance(r, TT.Runnable))
        self.assertEquals(r.name, TT.Runnable.name)

    def test_10__init__w_name_arg(self):
        name = "named_runnable"
        r = TT.Runnable(name)

        self.assertTrue(isinstance(r, TT.Runnable))
        self.assertNotEquals(r.name, TT.Runnable.name)
        self.assertEquals(r.name, name)

    def test_20__init__w_name_and_some_extra_args(self):
        name = "named_runnable"
        (a, b) = (1, 2)
        r = TT.Runnable(name, a=a, b=b)

        self.assertTrue(isinstance(r, TT.Runnable))
        self.assertEquals(r.a, a)
        self.assertEquals(r.b, b)


class Test_10_RunnableWithConfig(unittest.TestCase):

    def test_00__init__w_no_args(self):
        r = TT.RunnableWithConfig()

        self.assertTrue(isinstance(r, TT.RunnableWithConfig))
        self.assertEquals(r.name, TT.RunnableWithConfig.name)
        self.assertEquals(r.enabled, TT.RunnableWithConfig.enabled)

        fallback = random.random()
        self.assertEquals(r.getconf("a_missing_key", fallback), fallback)
        self.assertEquals(r.getconf("a.hierarchized.missing_key", fallback),
                          fallback)

    def test_10_getconf(self):
        name = TT.RunnableWithConfig.name
        conf = {name: dict(a=1, b=dict(c=3, d=dict(e=5,)))}
        r = TT.RunnableWithConfig(name, conf)

        self.assertEquals(r.getconf("a"), conf[name]["a"])
        self.assertEquals(r.getconf("b.c"), conf[name]["b"]["c"])
        self.assertEquals(r.getconf("b.d.e"), conf[name]["b"]["d"]["e"])

        fallback = random.random()
        self.assertEquals(r.getconf("a_missing_key", fallback), fallback)
        self.assertEquals(r.getconf("a.hierarchized.missing_key", fallback),
                          fallback)


class Test_20_RunnableWithIO(unittest.TestCase):

    def test_00__init__w_no_args(self):
        r = TT.RunnableWithIO()

        self.assertTrue(isinstance(r, TT.RunnableWithIO))
        self.assertEquals(r.input_paths, [])
        self.assertTrue(r._mk_output_path("a/b.txt"),
                        os.path.join(TT.RunnableWithIO.outputs_dir,
                                     "a/b.txt.json"))

    def test_02__init__w_list_inputs(self):
        r = TT.RunnableWithIO("/tmp", None, ["a.txt", "b/c.json"])

        self.assertTrue(isinstance(r, TT.RunnableWithIO))
        self.assertNotEquals(r.input_paths, [])
        self.assertEquals(r.input_paths, [("a.txt", "/tmp/a.txt"),
                                          ("b/c.json", "/tmp/b/c.json")])

    def test_04__init__w_list_inputs_and_ouptputs_dir(self):
        r = TT.RunnableWithIO("/tmp", "/tmp/outputs", ["a.txt", "b/c.json"])

        self.assertTrue(isinstance(r, TT.RunnableWithIO))
        self.assertNotEquals(r.input_paths, [])
        self.assertEquals(r.input_paths, [("a.txt", "/tmp/a.txt"),
                                          ("b/c.json", "/tmp/b/c.json")])
        self.assertEquals(r._mk_output_path("x/y/z.txt"),
                          "/tmp/outputs/x/y/z.txt.json")


# vim:sw=4:ts=4:et:
