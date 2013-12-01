sos-analyzer
============

A tool to scan and analyze data collected by sosreport

Build & Install
================

If you're Fedora or Red Hat Enterprise Linux user, try::

  $ python setup.py srpm && mock dist/SRPMS/python-sos-analyzer-<ver_dist>.src.rpm
    
    or::

  $ python setup.py rpm

and install built RPMs. 

Otherwise, try usual ways to build and/or install python modules such like
'easy_install anyconfig', 'python setup.py bdist', etc.

Meta
======

* Author: Satoru SATOH <ssato _at_ redhat.com>
* License: GPLv3+

.. vim:sw=2:ts=2:et:
