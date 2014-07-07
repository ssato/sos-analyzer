#
# Author: Satoru SATOH <ssato redhat.com>
# License: GPLv3+
#
import sos_analyzer.shell as SS
import os.path


class UnknownTarCompressorError(Exception):
    pass


def detect_compressor_opt(tarfile):
    """
    Detect compressor used for given tar archive and return appropriate tar
    option to extract it.

    TODO: Find out compressor not by file extension of given tar archive, maybe
    with using `file` program or something.

    :param tarfile: Tar archive file

    >>> detect_compressor_opt("/a/b/c/d.tar")
    ''
    >>> detect_compressor_opt("/a/b/c/d.tar.xz")
    '--xz'
    >>> detect_compressor_opt("/a/b/c/d.tar.bz2")
    '--bzip2'
    >>> detect_compressor_opt("/a/b/c/d.tar.gz")
    '--gzip'
    """
    try:
        ext = os.path.splitext(tarfile)[-1][1:]

        if ext == "tar":
            return ""  # no option needed as the tar file not compressed.
        elif ext == "xz":
            return "--xz"
        elif ext == "bz2":
            return "--bzip2"
        elif ext == "gz":
            return "--gzip"
        else:
            raise UnknownTarCompressorError(": " + tarfile)
    except:
        raise UnknownTarCompressorError(": " + tarfile)


def extract_archive(tarfile, destdir):
    """
    Extract given tar archive into ``destdir``.

    :param tarfile: Tar archive file
    :param destdir: Destination dir to extract given tar archive
    """
    compressor_opt = detect_compressor_opt(tarfile)
    cmd = "tar %s -xf %s -C %s" % (compressor_opt, tarfile, destdir)

    SS.run(cmd, stop_on_error=True)

# vim:sw=4:ts=4:et:
