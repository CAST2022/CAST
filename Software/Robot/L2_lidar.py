import os
import sys
import time
import RPi.GPIO as GPIO
import adafruit_rplidar as raslidar
from math import cos, sin, pi, floor
# from adafruit_rplidar import RPLidar,DEFAULT_MOTOR_PWM

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
    #    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data_angle[min([359, floor(angle)])] = angle
            scan_data_distance[min([359, floor(angle)])] = distance
        
        # Filters the data to be read between angles 219 and 360 from the core of the Lidar 
        if angle > 219 and angle < 360 and angle != 0:
            # Distance is in mm
            if distance > 500 and distance != 0:
                # Similates turning off the UV LEDs
                GPIO.output(18,GPIO.LOW)
                # print(distance)
                # print(angle)
                print("far")
            if distance <= 500 and distance != 0:
                # Simulates turning on the UV LEDs
                GPIO.output(18,GPIO.HIGH)
                # print(distance)
                # print(angle)
                print("close")
                
        else:
            pass
# Is included to safely turn off the Lidar system
except KeyboardInterrupt:
    print('Stopping.')
    lidar.stop()
    lidar.disconnect()
    
    # return data
