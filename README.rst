sos-analyzer
============

A tool to scan and analyze data collected by sosreport

Reference
----------

* sosreport: https://github.com/sosreport/sosreport
* checksysreport: http://ostatic.com/checksysreport
* sxconsole: https://fedorahosted.org/sx/
* xsos - sosreport examiner: https://github.com/ryran/xsos

Build & Install
================

If you're Fedora or Red Hat Enterprise Linux user, try::

  $ python setup.py srpm && mock dist/SRPMS/python-sos-analyzer-<ver_dist>.src.rpm
    
or::

  $ python setup.py rpm

and install built RPMs. 

Otherwise, try usual ways to build and/or install python modules such like
'python setup.py bdist', etc.

Requirements
-------------

sos-analyzer depends on python-anyconfig which is available from:

* https://github.com/ssato/python-anyconfig

It's able to build and make a package of python-anyconfig as same as
sos-analyzer. Plus, you may build and/or install anyconfig such like
'easy_install anyconfig', 'python setup.py bdist', etc.

How to hack
============

How to test
-------------

Try to run './aux/runtest.sh [path_to_python_code]'.

Test status
-------------

.. image:: https://api.travis-ci.org/ssato/sos-analyzer.png?branch=master
   :target: https://travis-ci.org/ssato/sos-analyzer
   :alt: Test status

Meta
======

* Author: Satoru SATOH <ssato _at_ redhat.com>
* License: GPLv3+

.. vim:sw=2:ts=2:et:
