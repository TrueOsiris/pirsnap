#!/usr/bin/python
"""
  Pirsnap 1.0 Motion sensed supervisor                                     
  Written by Tim Chaubet                                                                                                   #
                                                                           
  Requirements:                                                            
  - Python 2.7.3 with GCC 4.6.3                                            
  - Raspberry pi with raspbian, updated until at least 2014-09             
  - PIR motion sensor, output on pin 12                                    
  - Noir infrared camera module                                            
                                                                           
  Snapshots are taken according to a certain schedule OR when motion is    
  detected. For each day, a subfolder (format YYYY-MM-DD) is created       
  in which jpgs will arrive.                                               
  While motion is being detected, pictures will be taken at certain        
  definable intervals                                                      
                                                                           
  This program is free software: you can redistribute it and/or modify     
  it under the terms of the GNU General Public License as published by     
  the Free Software Foundation, either version 3 of the License, or        
  (at your option) any later version.                                      
  This program is distributed in the hope that it will be useful,          
  but WITHOUT ANY WARRANTY; without even the implied warranty of           
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the             
  GNU General Public License for more details.                             
  
"""

import RPi.GPIO as GPIO
import time
import os, sys, pwd, grp
from datetime import timedelta,datetime,date
import picamera
sensorPin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Base camera settings
camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.crop = (0.0, 0.0, 1.0, 1.0)
camera.resolution = (1920, 1080)

# Initialise modifiable variables
picPrefix = 'cam1_'             # prefix of the .jpg files
picPath = '/mnt/pics/'          # location where date-folders with snapshots will be stored
moSuffix = '_sensor'            # motion sensed pictures get this suffix
scSuffix = ''                   # scheduled pictures get this suffix
motionDelta=9                   # minimum seconds between motion detected pics
mins=('00','15','30','45')      # Scheduler in hours, mins: a picture is taken, regardless of motion sensed
hours=('05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21')
uid = pwd.getpwnam("nobody").pw_uid     # which user & group will the folders and .jpg files get
gid = grp.getgrnam("nogroup").gr_gid

# Initialise switches & program variables
prevState = False
currState = False
curmin = time.strftime('%M')    # 2-digit current minute
curhour = time.strftime('%H')   # 2-digit current hour
t = datetime.now() + timedelta(seconds=motionDelta)
cursec = t.strftime('%M%S')     # 4-digit current minute+second
check=0

# Save image to disk
def saveImage(suffix):                                  # all pics get suffix
    di = picPath + "/" + str(time.strftime("%Y-%m-%d")) # subdirectory name
    if not os.path.exists(di):                          # check whether dir exists
        os.mkdir(di, 0775)                              # create dir
        os.chown(di,uid,gid)                            # set user & group of dir
        os.chmod(di,0o775)                              # set rwx rights on dir
    picName = di + "/" + picPrefix + str(time.strftime("%Y-%m-%d_%Hh%M-%S")) + suffix + ".jpg"
    camera.capture(picName)                             # get snapshot & save to disk
    os.chown(picName,uid,gid)                           # change user & group of .jpg
    os.chmod(picName,0o775)                             # change rwx of .jpg

try:
    while GPIO.input(sensorPin)==1:                     # initialization of pin & state
        currState = 0
    while True:                                         # Will execute about 10 times per second
                                                        """ Scheduler check """
        if time.strftime('%M')==curmin:                 # Is this minute the one saved in 'curmin' ?
            if check==0:                                #  Has the current minute already been checked?
                if curmin in mins and curhour in hours: #   If not, check scheduled hours-mins.
                    saveImage(scSuffix)                 #    When this is a scheduled minute, take pic
            check=1
        else:                                           # Is this minute NOT the one saved in 'curmin' ?
            curmin = time.strftime('%M')                # Set this minute as the new 'curmin'
            curhour = time.strftime('%H')
            check=0
                                                        """ Motion sensor check """
        currState = GPIO.input(sensorPin)               # get sensor pin status. Gets 1 on detection.                                                        
        if currState==1 and prevState==0:               # Did the sensor just trigger ? if yes ...
            saveImage(moSuffix)                         #  Take a picture
            prevState=1                                 #  set previous-sensorcheck on
            t = datetime.now() + timedelta(seconds=motionDelta)
            cursec = t.strftime('%M%S')                 #  set 'cursec' to 'delta' seconds in the future
        elif currState==0 and prevState==1:             # if the sensor just un-trigger (no more motion) ...
            prevState=0                                 #  set previous-sensorcheck off
        if datetime.now() > t:                          # if beyond previously set future 'cursec' moment ...
            prevState=0                                 #  set previous-sensorcheck off anyway
            
except KeyboardInterrupt:
        GPIO.cleanup()
