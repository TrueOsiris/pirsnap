#! /bin/sh
### BEGIN INIT INFO
# Provides:          pirsnap
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Pirsnap Daemon
# Description:       Pirsnap takes motion sensed & scheduled pictures
### END INIT INFO
# Author: Tim Chaubet <tim@chaubet.be>

case "$1" in
  start)
    echo "Starting Pirsnap"
    # run application you want to start
    python /scripts/pirsnap.py &
    ;;
  stop)
    echo "Stopping Pirsnap"
    # kill application you want to stop
    killall python
    ;;
  restart)
    echo "Restarting Pirsnap"
    killall python
    #ps -AF | grep pirsnap
    python /scripts/pirsnap.py &
    #ps -AF | grep pirsnap
    ;;
  *)
    echo "Usage: /etc/init.d/pirsnap {start|stop|restart}"
    exit 1
    ;;
esac

exit 0
