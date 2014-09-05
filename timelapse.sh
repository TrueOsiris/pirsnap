#!/bin/sh
# requires mencoder & basename
# adapt basedir to your needs
#
thisdir=`pwd`
basedir=/mnt/documents/btsynced/cam1/
today=$(date +%Y-%m-%d)
curdir=$basedir$today
if [ $1 ]; then
        curdir=$1
fi
cd $curdir
dirname=`basename "$PWD"`
echo "Starting timelapse memcoder in "`pwd`
#ls -htr *.jpg > list.txt
find * -maxdepth 1 -iname "*.jpg" -type f ! -empty | sort -n > list.txt
mencoder -ovc lavc -lavcopts vcodec=msmpeg4v2:vpass=1:vbitrate=10125000:mbd=2:keyint=132:vqblur=1.0:cmp=2:subcmp=2:dia=2:mv0:last_pred=3 mf://@list.txt -mf fps=25:type=jpg -o "timelapse."$dirname".1920x1080.avi"
mencoder -ovc lavc -lavcopts vcodec=msmpeg4v2:vpass=1:vbitrate=2160000:mbd=2:keyint=132:vqblur=1.0:cmp=2:subcmp=2:dia=2:mv0:last_pred=3 mf://@list.txt -mf fps=25:type=jpg -o "timelapse."$dirname".768x576.avi"
rm list.txt
rm divx2pass.log
cd $thisdir
