#Imports
import  L2_speed_control as sc
import L2_inverse_kinematics as inv
from gpiozero import SmoothedInputDevice as tof
from gpiozero import DigitalOutputDevice as uv
from gpiozero import Motor as act

#Run main loop
while True:
    #GamePad Control
    def manual_nav():
        c = inv.getPdTargets()
        sc.driveOpenLoop(c)

    while 1:
        manual_nav()
        time.sleep(0.02)

    #RPLIDAR
    # Setup the RPLidar
    PORT_NAME = '/dev/ttyUSB0'
    lidar = RPLidar(None, PORT_NAME)

    print(lidar.get_info())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)

    #ToF
    leftsensor = tof(16, active_high=True)
    rightsensor = tof(20, active_high=True)
    bottomsensor = tof(21, active_high=False)

    # Keep all low for 500 ms or so to make sure they reset
    time.sleep(0.50)

    leftsensor = VL53L0X.VL53L0X(i2c_address=0x2B)
    rightsensor = VL53L0X.VL53L0X(i2c_address=0x2D)
    bottomsensor = VL53L0X.VL53L0X(i2c_address=0x2E)

    leftsensor.open()
    rightsensor.open()
    bottomsensor.open()

    # Set shutdown pin high for the first VL53L0X then
    # call to start ranging
    time.sleep(0.50)
    leftsensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

    # Set shutdown pin high for the second VL53L0X then
    # call to start ranging
    time.sleep(0.50)
    rightsensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

    #Lidar Functionality
    distance = lidar.scan[::3]
    if distance < 15:  # inches
        Lights = uv(4, active_high=True)
    else:
        Lights = uv(4,active_high=False)

    #ToF Functionality
    A = leftsensor.get_distance()
    B = rightsensor.get_distance()
    if A<20:
        motor = act(6,12)
        motor.forward()
        bottomsensor = tof(21, active_high=True)
        time.sleep(0.50)
        bottomsensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
        if C>20:
            motor.backward()
            if C<20:
                motor.stop()
    if B<20:
        motor = act(6,12)
        motor.forward()
        bottomsensor = tof(21, active_high=True)
        time.sleep(0.50)
        bottomsensor.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
        if C>20:
            motor.backward()
            if C<20:
                motor.stop()
