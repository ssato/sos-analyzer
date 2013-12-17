from setuptools import setup, Command, find_packages
from distutils.sysconfig import get_python_lib
from glob import glob

import os.path
import os
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
    cmd_fmt = """rpmbuild -b%(build_stage)s \
        --define \"_topdir %(rpmdir)s\" \
        --define \"_sourcedir %(rpmdir)s\" \
        --define \"_buildroot %(BUILDROOT)s\" \
        %(rpmspec)s
    """

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.update_mo()
        self.run_command('sdist')
        self.build_rpm()

    def update_mo(self):
        os.system("./aux/update-po.sh")

    def build_rpm(self):
        params = dict()

        params["build_stage"] = self.build_stage
        rpmdir = params["rpmdir"] = os.path.join(os.path.abspath(os.curdir),
                                                 "dist")
        rpmspec = params["rpmspec"] = \
            os.path.join(rpmdir, "../%s.spec" % PACKAGE)

        for subdir in ("SRPMS", "RPMS", "BUILD", "BUILDROOT"):
            sdir = params[subdir] = os.path.join(rpmdir, subdir)

            if not os.path.exists(sdir):
                os.makedirs(sdir, 0o755)  # 493 = 0o755 (py3) or 0755 (py2)

        c = open(rpmspec + ".in").read()
        open(rpmspec, "w").write(c.replace("@VERSION@", VERSION))

        os.system(self.cmd_fmt % params)


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
