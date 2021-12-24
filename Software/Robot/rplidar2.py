"""
Slamtec RPLIDAR library for CircuitPython.
Adapted from https://github.com/SkoltechRobotics/rplidar
Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!
Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.
All text above must be included in any redistribution.
"""

import os
import sys
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

scan_data = [0]*360

def _process_scan(raw):
    '''Processes input raw data and returns measurment data'''
    new_scan = bool(raw[0] & 0b1)
    inversed_new_scan = bool((raw[0] >> 1) & 0b1)
    quality = raw[0] >> 2
    if new_scan == inversed_new_scan:
        raise RPLidarException('New scan flags mismatch')
    check_bit = raw[1] & 0b1
    if check_bit != 1:
        raise RPLidarException('Check bit not equal to 1')
    angle = ((raw[1] >> 1) + (raw[2] << 7)) / 64.
    distance = (raw[3] + (raw[4] << 8)) / 4.
    return new_scan, quality, angle, distance

def lidar_measurments(self, max_buf_meas=500):

    lidar.set_pwm(800)
    status, error_code = self.health

    cmd = SCAN_BYTE
    self._send_cmd(cmd)
    dsize, is_single, dtype = self._read_descriptor()
    if dsize != 5:
            raise RPLidarException('Wrong info reply length')
    if is_single:
            raise RPLidarException('Not a multiple response mode')
    if dtype != SCAN_TYPE:
            raise RPLidarException('Wrong response data type')
    while True:
        raw = self._read_response(dsize)
        self.log_bytes('debug', 'Received scan response: ', raw)
        if max_buf_meas:
            data_in_buf = self._serial_port.in_waiting
            if data_in_buf > max_buf_meas * dsize:
                self.log('warning',
                        'Too many measurments in the input buffer: %d/%d. '
                        'Clearing buffer...' %
                        (data_in_buf // dsize, max_buf_meas))
                self._serial_port.read(data_in_buf // dsize * dsize)
        yield _process_scan(raw)

def lidar_scans(self, max_buf_meas=500, min_len=5):
    scan = []
    iterator = lidar_measurments(lidar, max_buf_meas)
    for new_scan, quality, angle, distance in iterator:
        if new_scan:
            if len(scan) > min_len:
                yield scan
            scan = []
        if quality > 0 and distance > 0:
            scan.append((quality, angle, distance))
