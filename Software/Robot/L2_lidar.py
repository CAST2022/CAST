# Rplidar program for communicating with UV LEDs
# This code sends power to the power relay on the appropriate GPIO pins for turning on the UV LEDs
# Last update 3/25/2022 - Edgar Macias

import os
import sys
import time
import RPi.GPIO as GPIO
import adafruit_rplidar as raslidar
from math import cos, sin, pi, floor

#Setup LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = raslidar.RPLidar(None, PORT_NAME, timeout=3)

# Setup the data info for 360 degrees around the core of the Lidar
scan_data_angle = [0] * 360
scan_data_distance = [0] * 360

# Continuously runs at all times, unless keyboard interrupts the program
try:
    # print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data_angle[min([359, floor(angle)])] = angle
            scan_data_distance[min([359, floor(angle)])] = distance
        
        # Filters the data to be read between angles 219 and 360 from the core of the Lidar 
        if angle > 219 and angle < 360 and angle != 0:
            # Distance is in mm
            # This if statement is important to control the UV LEDs
            # When the Lidar detects an object further than the length of the arm (508 mm) the program will turn off the UV LEDs
            if distance > 508 and distance != 0:
                # Simulates turning off the UV LEDs
                GPIO.output(18,GPIO.LOW)
            # When the Lidar detects an object within the length of the arm, the program will turn on the UV LEDs
            if distance <= 508 and distance != 0:
                # Simulates turning on the UV LEDs
                GPIO.output(18,GPIO.HIGH)
        else:
            pass
# Is included to safely turn off the Lidar system
except KeyboardInterrupt:
    print('Stopping.')
    lidar.stop()
    lidar.disconnect()
    
    # return data
