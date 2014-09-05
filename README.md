pirsnap
=======

Pirsnap - Surveillance Cam python script for Raspberry pi + Noir cam + PIR motion sensor

Requirements:                                                            
- Python 2.7.3 with GCC 4.6.3                                            
- Raspberry pi with raspbian, updated until at least v14
- PIR motion sensor, output on pin 12                                    
- Noir infrared camera module                                            

Snapshots are taken according to a certain schedule OR when motion is detected. For 
each day, a subfolder (format YYYY-MM-DD) is created in which jpgs will arrive.                                         
While motion is being detected, pictures will be taken at certain definable intervals.

Instructions:
- Put the pirsnap.py in /scripts/ (or change the path in the init.d script)
  pirsnap.py can be run from command line as is.
- Put the init.d script in /etc/init.d/ and rename it to 'pirsnap'
- To autostart run: update-rc.d pirsnap defaults
 
Notes:
- Due to constant motion sensor checking & scheduler, the cpu usage peaks.
  The program basically takes up all the cpu, to do as many checks as possible
  per second.
- The script does not contain a diskcheck and file cleanup anymore.
  I've installed bittorrent sync and had it sync the /mnt/pics folder to my nas.
  From these I create timelapse vids and I move the actual jpgs elsewhere, hence 
   keeping my rasp clean. It has a 64GB sd anyway, so it can hold about 2 months
   without touching the folder. 
- On the nas where the pics arrive btsynced, I have 2 cronjobs:<br>
   59 23 * * * /bin/timelapse<br>
   00 01 * * * /bin/timelapse_full<br>
  These create timelapse avi's using mencoder. I've added the bash scripts.
- I'm using 2 rasps as a construction site supervisor as anti-theft system and
  to create a timelapse video of our house being built.
 
In development: 
- measure daylight & go for a longer exposure when it gets darker.
