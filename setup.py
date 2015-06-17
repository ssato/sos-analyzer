from setuptools import setup, Command, find_packages
from distutils.sysconfig import get_python_lib
from glob import glob

import os.path
import os
import subprocess
import sys

curdir = os.getcwd()
sys.path.append(curdir)

PACKAGE = "sos-analyzer"
VERSION = "0.0.2"

# For daily snapshot versioning mode:
if os.environ.get("_SNAPSHOT_BUILD", None) is not None:
    import datetime
    VERSION = VERSION + datetime.datetime.now().strftime(".%Y%m%d")


def list_files(tdir):
    return [f for f in glob(os.path.join(tdir, '*')) if os.path.isfile(f)]


data_files = [  # (destdir, list_files(srcdir),
    (os.path.join(get_python_lib(), "sos_analyzer/locale/ja/LC_MESSAGES"),
     glob("sos_analyzer/locale/ja/LC_MESSAGES/*.mo")),
]


class SrpmCommand(Command):

    user_options = []
    build_stage = "s"

    curdir = os.path.abspath(os.curdir)
    rpmspec = os.path.join(curdir, "pkg/package.spec")

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.pre_sdist()
        self.run_command('sdist')
        self.build_rpm()

    def pre_sdist(self):
        c = open(self.rpmspec + ".in").read()
        open(self.rpmspec, "w").write(c.replace("@VERSION@", VERSION))

    def build_rpm(self):
        rpmbuild = os.path.join(self.curdir, "pkg/rpmbuild-wrapper.sh")
        workdir = os.path.join(self.curdir, "dist")

        cmd_s = "%s -w %s -s %s %s" % (rpmbuild, workdir, self.build_stage,
                                       self.rpmspec)
        subprocess.check_call(cmd_s, shell=True)


class RpmCommand(SrpmCommand):

    build_stage = "b"


setup(name=PACKAGE,
      version=VERSION,
      description="A tool to scan and analyze data collected by sosreport",
      author="Satoru SATOH",
      author_email="ssato@redhat.com",
      license="GPLv3+",
      url="https://github.com/ssato/sos-analyzer",
      packages=find_packages(),
      include_package_data=True,
      scripts=glob("tools/*"),
      data_files=data_files,
      cmdclass={"srpm": SrpmCommand, "rpm":  RpmCommand, },
      )

# vim:sw=4:ts=4:et:
