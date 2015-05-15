#! /bin/bash
set -ex

pkgname="sos_analyzer"

auxdir=${0%/*}
topdir=${auxdir}/../
podir=${topdir}/po
localedir=${topdir}/${pkgname}/locale

pygettext.py -d ${pkgname} -p ${podir} $(find ${topdir}/${pkgname} -name '*.py' | grep -v test)

for po in ${podir}/*.po; do
    t=${po##*/}
    lang=${t/.po/}
    locdir=${localedir}/${lang}/LC_MESSAGES

    test -d ${locdir} || mkdir -p ${locdir}

    msgmerge  --update ${po} ${podir}/${pkgname}.pot
    msgfmt -v ${po} -o ${locdir}/${pkgname}.mo
done
