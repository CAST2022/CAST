# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.
import time
import board
import busio
import adafruit_vl53l0x

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

#Move variable will output zero or one to communicate when the arm needs to move
Move = 0
# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

# Main loop will read the range and print it every second.
while True:
    ToF1=int(vl53.range)
    print("Range: {0}mm".format(vl53.range))
    if ToF1<500:
        #Move variable will output zero or one to communicate when the arm needs to move
        #This is the variable that will be used in the linear actuator program
        move = 1
        print(move)
    else:
        move = 0
        print(move)
    time.sleep(0.005)
