pirsnap
=======

Pirsnap - Surveillance Cam python script for Raspberry pi + Noir cam + PIR motion sensor

Instructions:
- Put the pirsnap.py in /scripts/ (or change the path in the init.d script)
- put the init.d script in /etc/init.d/ and rename it to 'pirsnap'
- To autostart run: update-rc.d pirsnap defaults

This script does not contain a diskcheck and file cleanup anymore.
I've installed bittorrent sync and had it sync the /mnt/pics folder to my nas.
From these I create timelapse vids and I move the actual jpgs elsewhere, hence 
 keeping my rasp clean. It has a 64GB sd anyway, so it can hold about 2 months
 without touching the folder.
 
Notes :
- Due to constant motion sensor checking & scheduler, the cpu usage peaks.
  The program basically takes up all the cpu, to do as many checks as possible
  per second.
 
In development : 
- measure daylight & go for a longer exposure when it gets darker.
