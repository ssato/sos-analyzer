#! /bin/bash
set -e


testsdir=${0%/*}
topdir=../$testsdir

which pep8 2>&1 > /dev/null && check_with_pep8=1 || check_with_pep8=0

if test $# -gt 0; then
    test $check_with_pep8 = 1 && (for x in $@; do pep8 ${x%%:*}; done) || :
    PYTHONPATH=$topdir nosetests -c $testsdir/nose.cfg $@
else
    #PYTHONPATH=$topdir nosetests -c $testsdir/nose.cfg -w $testsdir
    echo "Usage: $0 DIR_OR_PYTHON_FILE_0[ DIR_OR_PYTHON_FILE_1 ...]"
fi
