# L1 program for CAST Bot actuator runnning SCUTTLE RasPi image
# This code sends signals to ST-M5045 motor driver/NEMA 23 stepper motor on appropriate GPIO pins
# See wiring guide doncument for pin mapping
# Last update 04.12.2022 - Kenneth Grau

# Import external libraries

# note pigpio uses BROADCOM numbers for labeling
import pigpio

# sleep is used for precision stepping as timing has a resolution of 1ms
import time
from time import sleep

# Initialize pigpio
pi = pigpio.pi()

# label signal pins
puls = 13
dir = 19
en = 26

# Label endstop pins
topEndStop = 5
botEndStop = 6

# Setup mode for GPIO pins
pi.set_mode(puls, pigpio.OUTPUT)            # pulse/signal generation
pi.set_mode(dir, pigpio.OUTPUT)             # direction pin
pi.set_mode(en, pigpio.OUTPUT)              # enable pin (active low)
pi.set_mode(topEndStop, pigpio.INPUT)       # enable pin (active low)
pi.set_mode(botEndStop, pigpio.INPUT)       # enable pin (active low)


# Set of parameters preset by user determined by actuator and driver
linearDistancePerRev = 0.00508  # lead as specified by actuator ball screw datasheet (m)
stepsPerRev = 800               # steps per revolution per driver
maxPrecisionSpeed = 0.00635
maxSpeed = 0.09525


# Move arm in a specified direct at specified speed with precision stepping
def stepMove(dist, dirs, speed = maxPrecisionSpeed):
    
    pi.set_mode(puls, pigpio.OUTPUT)                        # Ensure pin is in correct mode and setup enable
    pi.write(en,0)
    
    if (dirs == 1):                                         # Set direction based on input
        pi.write(dir,1)
    else:
        pi.write(dir,0)
    
    steps = dist / linearDistancePerRev * stepsPerRev       # Calculate steps needed to travel desired distance
    
    delay = 1/(speed/linearDistancePerRev*stepsPerRev)/2    # Calculate delay for desired speed
    
    for x in range(int(steps)):
        pi.write(puls,0)
        sleep(delay)
        pi.write(puls,1)
        sleep(delay)
        
    pi.write(en,1)
            
# Move the arm in direction with specified speed (less precise but much faster)
def pwmMove(dist, dirs, speed = maxSpeed):
    
    pi.write(en,0)
    x = 0
    
    if (dirs == 1):                                     # Set direction based on input
        pi.write(dir,1)
    else:
        pi.write(dir,0)
    
    freq = speed / linearDistancePerRev * stepsPerRev   # Calculate frequency for desired speed
    
    delay = (dist / speed) + (freq / 100 * 0.001)       # Calculate wait for certain distance
    if (delay < 0):
        delay = 0
    
    while(x <= freq):                                   # Ramp up to speed (maybe replace with log ramping)
        pi.hardware_PWM(puls,x,50000)
        sleep(0.001)
        x = x + 100
    time.sleep(delay)                                   # Let pwm drive for certain amount of time
    
    pi.hardware_PWM(puls, 0, 0)                         # Turn off PWM
    pi.write(en,1)
        
# Reset actuator arm to bottom position
def resetArm():

    pi.write(en,0)
    pi.write(dir,0)
    x = 0
    
    while(x <= 15000):                                  # Ramp up to speed (maybe replace with log ramping)
        pi.hardware_PWM(puls,x,50000)
        sleep(0.001)
        x = x + 100

# Callback function for handling top endstop trigger       
def topEndStopHandle():

    pi.set_mode(puls, pigpio.OUTPUT)
    pi.write(dir,0)
    pi.write(en,0)
    
    while (pi.read(topEndStop) == 1):                   # Move arm off endstop
        pi.write(puls,0)
        sleep(0.0001)
        pi.write(puls,1)
        sleep(0.0001)
        
    pi.write(en,1)


# Callback function for handling bottom endstop trigger
def botEndStopHandle():

    pi.set_mode(puls, pigpio.OUTPUT)
    pi.write(dir,1)
    
    while (pi.read(botEndStop) == 1):                   # Move arm off endstop
        pi.write(puls,0)
        sleep(0.0001)
        pi.write(puls,1)
        sleep(0.0001)
        
# Setup inturrupts for handling endstops
topStop = pi.callback(5, pigpio.RISING_EDGE, topEndStopHandle)
topStop = pi.callback(6, pigpio.RISING_EDGE, botEndStopHandle)

if __name__ == "__main__":
    
    print('Resetting arm to bottom position...')
    resetArm()
    
    print('Precision move up 1cm')
    stepMove(0.01,1)
    print('Precision move down 1cm')
    stepMove(0.01,0)
    
    print('Speed move up 10cm')
    pwmMove(0.1,1)
    print('Speed move down 10cm')
    pwmMove(0.1,0)
