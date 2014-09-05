#!/bin/sh
thisdir=`pwd`
basedir=/mnt/documents/btsynced/cam1/
cd $basedir
find * -mindepth 1 -iname "*1920x1080.avi" -type f ! -empty | sort -n > avilist.txt
mencoder -forceidx -ovc copy -oac copy -o 1920x1080.avi `cat avilist.txt`
find * -mindepth 1 -iname "*576.avi" -type f ! -empty | sort -n > avilist.txt
mencoder -forceidx -ovc copy -oac copy -o 768x576.avi `cat avilist.txt`
rm avilist.txt
cd $thisdir
