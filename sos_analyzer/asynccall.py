#
# Copyright (C) 2013 Red Hat, Inc.
# Red Hat Author(s): Satoru SATOH <ssato@redhat.com>
# License: GPLv3+
#
import logging
import multiprocessing
import os
import os.path
import signal


LOGGER = logging.getLogger(__name__)

_RUN_TO = None
_NPROC = multiprocessing.cpu_count() * 2


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


def _killpg(pgid, sig=signal.SIGKILL):
    return os.killpg(pgid, sig)


def spawn(func, func_args=[], func_kwargs={}, **kwargs):
    """
    :param func: Function or any callable in global scope
    :param func_args: Arguments for the function ``func``
    :param func_kwargs: Keyword arguments for the function ``func``

    :return: multiprocessing.Process instance
    """
    return multiprocessing.Process(target=func, args=func_args,
                                   kwargs=func_kwargs)


def call_async(func, func_args=[], func_kwargs={}, **kwargs):
    """
    Call function w/o blocking (asynchronously).

    :param func: Function or any callable in global scope
    :param func_args: Arguments for the function ``func``
    :param func_kwargs: Keyword arguments for the function ``func``

    :return: multiprocessing.Process instance
    """
    logging.debug("Call: f=%s, args=%s, kwargs=%s" % (str(func),
                                                      str(func_args),
                                                      str(func_kwargs)))
    proc = spawn(func, func_args, func_kwargs)
    proc.start()

    # Hacks:
    setattr(proc, "function", func)

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

    >>> import time
    >>> p = call_async(time.sleep, (1, ))
    >>> time.sleep(2)  # wait for the completion of the above.
    >>> _force_stop_proc(p)
    True
    >>> _force_stop_proc(call_async(time.sleep, (10, )))
    False
    """
    if not proc.is_alive():
        return val0  # TODO: Nothing to do but what it should return ?

    proc.terminate()
    if not proc.is_alive():
        return val0

    os.kill(proc.pid, signal.SIGKILL)
    return val1


def stop_async_call(proc, timeout=_RUN_TO, stop_on_error=False):
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

    m = "Failed (%s): %s" % (reason, str(proc.function))

    if stop_on_error:
        raise RuntimeError(m)

    logging.warn(m)
    return False

# vim:sw=4:ts=4:et:
