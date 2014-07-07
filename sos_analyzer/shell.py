#
# Copyright (C) 2011 - 2013 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato@redhat.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import sos_analyzer.compat as SC
import logging
import multiprocessing
import os
import os.path
import signal
import subprocess
import sys


def _validate_timeout(timeout):
    """
    Validate timeout value.

    >>> _validate_timeout(10)
    >>> _validate_timeout(0)
    >>> _validate_timeout(None)
    >>> try:
    ...     _validate_timeout(-1)
    ... except AssertionError:
    ...     pass

    :param timeout: Time value :: Int or None
    """
    assert timeout is None or int(timeout) >= 0, \
        "Invalid timeout: " + str(timeout)


def _validate_timeouts(*timeouts):
    """
    A variant of the above function to validate multiple timeout values.

    :param timeouts: List of timeout values :: [Int | None]
    """
    for to in timeouts:
        _validate_timeout(to)


def _killpg(pgid, sig=signal.SIGKILL):
    return os.killpg(pgid, sig)


def _run(cmd, workdir, rc_expected=0, logfile=False, **kwargs):
    """
    subprocess.Popen wrapper to run command ``cmd``. It will be blocked.

    An exception subprocess.CalledProcessError will be raised if
    the rc does not equal to the expected rc.

    :param cmd: Command string
    :param workdir: Working dir
    :param rc_expected: Expected return code of the command run
    :param logfile: Dump log file if True or log file path is specified or
        logfile is callable which generate log filename.
    :param kwargs: Extra keyword arguments for subprocess.Popen
    """
    assert os.path.exists(workdir), "Working dir %s does not exist!" % workdir
    assert os.path.isdir(workdir), "Working dir %s is not a dir!" % workdir

    ng_keys = ("cwd", "shell", "stdout", "stderr", "close_fds")
    kwargs = dict(((k, v) for k, v in SC.iteritems(kwargs)
                   if k not in ng_keys))
    rc = None
    try:
        proc = subprocess.Popen(cmd, cwd=workdir, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                close_fds=True,
                                **kwargs)

        if logfile:
            if isinstance(logfile, bool):
                logfile = os.path.join(workdir, "%d.log" % proc.pid)
            elif callable(logfile):
                logfile = logfile()

            logging.debug("cmd=%s, logfile=%s" % (cmd[:100], logfile))

            flag = 'a' if os.path.exists(logfile) else 'w'
            with open(logfile, flag) as f:
                for line in iter(proc.stdout.readline, ''):
                    f.write(line)
        else:
            for line in iter(proc.stdout.readline, ''):
                sys.stdout.write(line)

        if proc.wait() == rc_expected:
            return

        m = "Failed to run command: %s [%s]" % (cmd, workdir)
        raise RuntimeError(m)

    except subprocess.CalledProcessError as e:
        if rc and rc == rc_expected:
            return  # Not an error.

        raise RuntimeError(str(e))  # Raise ex again.


def _spawn(cmd, workdir, rc_expected=0, logfile=True, **kwargs):
    """
    :param cmd: Command string
    :param workdir: Working dir
    :param rc_expected: Expected return code of the command run
    :param logfile: Dump log file if True or its log file path
    :param kwargs: Extra keyword arguments for subprocess.Popen
    """
    return multiprocessing.Process(target=_run,
                                   args=(cmd, workdir, rc_expected, logfile),
                                   kwargs=kwargs)


# Connection timeout and Timeout to wait completion of runnign command in
# seconds. None or -1 means that it will wait forever.
_RUN_TO = None
_CONN_TO = 10


def bind(cmd1, cmd2, workdir1=os.curdir, workdir2=os.curdir):
    """
    >>> (c, d) = bind("true", "false")
    >>> c
    'true && false'

    >>> bind("true", "false", "/tmp", "/")
    ('true && cd / && false', '/tmp')
    """
    if workdir1 == workdir2:
        return ("%s && %s" % (cmd1, cmd2), workdir1)
    else:
        return ("%s && cd %s && %s" % (cmd1, workdir2, cmd2), workdir1)


def join(*cs):
    """
    :param cs: List of command strings.

    NOTE: workdir is same in all comamnds.

    >>> join("true", "false", "cd /tmp && yes")
    'true && false && cd /tmp && yes'
    """
    return " && ".join(cs)


def run_async(cmd, workdir=os.curdir, rc_expected=0, logfile=False, **kwargs):
    """
    Run command ``cmd`` asyncronously.

    :param cmd: Command string
    :param workdir: Working directory in which command runs
    :param rc_expected: Expected return code of the command run
    :param logfile: Dump log file if True or its log file path

    :return: multiprocessing.Process instance
    """
    logging.debug("Run: cmd=%s, cwd=%s" % (cmd[:100], workdir))
    proc = _spawn(cmd, workdir, rc_expected, logfile, **kwargs)
    proc.start()

    # Hacks:
    setattr(proc, "cmd", cmd)
    setattr(proc, "cwd", workdir)

    return proc


def _force_stop_proc(proc, val0=True, val1=False):
    """
    Force stopping the given process ``proc`` and return termination was
    success or not.

    :param proc: An instance of multiprocessing.Process.
    :param val0: Return value if the process was successfully terminated.
    :param val1: Return value if the process was failed to be terminated
        and then killed.

    :return: val0 or val1 according to conditions (see above).

    >>> p = run_async("true")
    >>> import time; time.sleep(2)  # wait for the completion of the above.
    >>> _force_stop_proc(p)
    True
    >>> _force_stop_proc(run_async("sleep 10"))
    False
    """
    if not proc.is_alive():
        return val0  # TODO: Nothing to do but what it should return ?

    proc.terminate()
    if not proc.is_alive():
        return val0

    os.kill(proc.pid, signal.SIGKILL)
    return val1


def stop_async_run(proc, timeout=_RUN_TO, stop_on_error=False):
    """
    Stop the given process ``proc`` spawned from function ``run_async``.

    :param proc: An instance of multiprocessing.Process
    :param timeout: Command execution timeout in seconds or None
    :param stop_on_error: Stop and raise exception if any error occurs

    :return: True if job was sucessful else False or RuntimeError exception
        raised if stop_on_error is True
    """
    _validate_timeout(timeout)
    assert isinstance(proc, multiprocessing.Process), \
        "Invalid type of 'proc' parameter was given!"

    try:
        proc.join(timeout)

        if proc.is_alive():
            reason = _force_stop_proc(proc, "timeout", "timeout-and-killed")
        else:
            if proc.exitcode == 0:
                return True  # Exit at once w/ successful status code.

            reason = "other"

    except (KeyboardInterrupt, SystemExit):
        reason = _force_stop_proc(proc, "interrupted", "interrupt-and-killed")

    m = "Failed (%s): %s" % (reason, proc.cmd)

    if stop_on_error:
        raise RuntimeError(m)

    logging.warn(m)
    return False


def run(cmd, workdir=os.curdir, rc_expected=0, logfile=False, timeout=_RUN_TO,
        stop_on_error=False, **kwargs):
    """
    Run command ``cmd``.

    >>> run("true")
    True
    >>> run("false")
    False

    >>> run("sleep 10", timeout=1)
    False

    :param cmd: Command string
    :param workdir: Working directory in which command runs
    :param rc_expected: Expected return code of the command run
    :param logfile: Dump log file if True or its log file path
    :param timeout: Command execution timeout in seconds or None
    :param stop_on_error: Stop and raise exception if any error occurs

    :return: True if job was sucessful else False or RuntimeError exception
        raised if stop_on_error is True
    """
    proc = run_async(cmd, workdir, rc_expected, logfile, **kwargs)
    return stop_async_run(proc, timeout, stop_on_error)


_NPROC = multiprocessing.cpu_count() * 2


def pmap(f, largs, nproc=_NPROC):
    """
    multiprocessing.Pool.map wrapper.

    FIXME: How to handle signals like KeyboardInterrupt exception (INT) ?

    :param f: Function to run in parallel
    :param largs: List of arguments passed to f. BTW, the arity of ``f`` must
        be 1 due to the restriction of the implementation of
        multiprocessing.Pool.map.
    :param nproc: Number of process to run in the pool

    :return: List of results of processes

    >>> import operator
    >>> pmap(operator.abs, [0, -1, 2, -3, -4], 3)
    [0, 1, 2, 3, 4]
    """
    assert callable(f), "``f`` must be any callable object!"
    return multiprocessing.Pool(processes=nproc).map(f, largs)


def _stop_async_run(pts):
    """
    Just an wrapper for ``stop_async_run`` to make it work w/
    multiprocessing.Pool.map.

    :param pts: A tuple of (proc, **kwargs) where kwargs is keyword arguments
        for ``stop_async_run``
    :return: Same as ``stop_async_run``

    >>> _stop_async_run((run_async("true"), dict(timeout=2, )))
    True
    >>> _stop_async_run((run_async("sleep 10"), dict(timeout=1, )))
    False
    """
    (proc, kwargs) = pts if len(pts) > 1 else (pts[0], {})
    return stop_async_run(proc, **kwargs)


def pstop_async_run(ps, timeout=_RUN_TO, stop_on_error=False):
    """
    Stop the given processes ``ps`` spawned from function ``run_async`` or
    ``prun_async``.

    :param ps: List of multiprocessing.Process instances previously started
    :param timeout: Command execution timeout in seconds or None
    :param stop_on_error: Stop and raise exception if any error occurs

    :return: List of result codes

    # TODO:
    #>>> pstop_async_run([run_async("true") for _ in range(4)], 2)
    #[True, True]
    """
    kwargs = dict(timeout=timeout, stop_on_error=stop_on_error)
    return pmap(_stop_async_run, ((p, kwargs) for p in ps))


def prun_async(cs, **kwargs):
    """
    :param cs: List of command strings
    :return: List of multiprocessing.Process instances
    """
    return [run_async(c, **kwargs) for c in cs]


def prun(cs, kwargs1={}, kwargs2={}, safer=True):
    """
    :param cs: List of command strings
    :param kwargs1: Keyword arguments passed to prun_async (run_async)
    :param kwargs2: Keyword arguments passed to stop_async_run
    :param safer: Do not use pstop_async_run if True (it would be slower but
        safer I guess).
    :param logdir: Logging dir. Each process will dump log files with
        dynamically generated filenames.

    :return: List of result code of run commands

    >>> prun(["true" for _ in range(3)], safer=True)
    [True, True, True]
    """
    if safer:
        return [stop_async_run(p, **kwargs2) for p in
                prun_async(cs, **kwargs1)]
    else:
        return pstop_async_run(prun_async(cs, **kwargs1), **kwargs2)


# vim:sw=4:ts=4:et:
