#!/bin/bash
VERSION=$1

rm release -rf
mkdir release
cp src/* release/ -r

rm release/locale
cp locale release/locale -r

rm release/ui
mkdir -p release/ui/img
cp res/img/ release/ui/ -r

cp bundle/* release/
cp sdk/weibo.py release/

cp LICENSE release/

rm -r release/*.pyc
rm -r release/*pycache*

tar -jcvf WeCase-${VERSION}.tar.bz2 release/
