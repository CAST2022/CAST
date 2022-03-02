import os
import sys
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)


# def process_data_distance(data):
#     print(data)

# print("new")

def process_data_angle(data):
    print(data)

scan_data_angle = [0] * 360
scan_data_distance = [0] * 360

try:
    #    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data_angle[min([359, floor(angle)])] = angle
            scan_data_distance[min([359, floor(angle)])] = distance
        # newdistance = process_data_distance(scan_data_distance)
        process_data_angle(scan_data_angle)
        
        length = len(scan_data_angle)
        length = length - 1
        i = -1
        while i < length:
            i = i + 1
            if scan_data_angle[i] >= 180:
                "testing side"
                if scan_data_distance[i] > 508:
                    print("OFF")
                else:
                    print("Lights On")
        


except KeyboardInterrupt:
    print('Stopping.')
lidar.stop()
lidar.disconnect()
