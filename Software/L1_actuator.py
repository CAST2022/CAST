# Motor program for CAST Bot actuator runnning SCUTTLE RasPi image
# This code sends commands to NEMA 23 stepper motor on appropriate GPIO pins for ST-M5045 Driver
# See wiring guide doncument for pin mapping
# Last update 03.24.2022 - Kenneth Grau

# Import external libraries
import gpiozero
from gpiozero import LED
from gpiozero import Button
from gpiozero import PWMOutputDevice as pwm
import time
from time import sleep

# Setup GPIO pins as output pins (probably could change to generic output deivce and use toggle)
en = LED(26)	    	    # enable pin always on
dir = LED(19)  		    # direction GPIO pin - on = cw (up), off = ccw(down)
step = LED(13)  	    # step GPIO pin

# Endstop pin assignment for integration of endstops as they are included on actuator
topEndStop = Button(6)
botEndStop = Button(5)

# Set of parameters preset by user determined by actuator used
linearDistancePerRev = 0.00508  # value determined by actuator screw (m)
stepsPerRev = 800               # steps per revolution per driver
maxMotorSpeed = 1100            # max motor speed in RPM
maxLinearSpeed = 0.01           # maximum speed in RPM by motor datasheet

# Calculate minimum delay for pulse
minDelay = 1/(maxMotorSpeed/60*stepsPerRev)/2


step.off()
en.off()

# Attempt at driving motor by generating PWM signal (not functioning)
#frq = maxSpeed/60*stepsPerRev
#step = pwm(13,frequency=frq,initial_value=0)


# Move arm in a specified direct at specified speed
def move(dist, dir, speed = maxLinearSpeed):
    
    # Set direction based on input
    if (dir == "up"):
        dir.off()
    else:
        dir.on()
        
    # Calcualte the delay required for specified speed and steps required
    steps = dist/linearDistancePerRev*stepsPerRev
    delay = 1/(speed/linearDistancePerRev*stepsPerRev)/2
    
    
    for x in range(int(steps)): 
       if not botEndStop.is_pressed:        # Check for endstop
            step.on()
            sleep(delay)
            step.off()
            sleep(delay)

def reset():
    rev = 20
    
    dir.on()  # switch directions
    en.off()
    
    #Calculate steps
    steps = rev * stepsPerRev

    for x in range(steps):  # rotate one revolution full checking endstops after steps
        if botEndStop.is_pressed:
            break
        step.on()
        sleep(minDelay)
        step.off()
        sleep(minDelay)
        



if __name__ == "__main__":

    dir.off()                            # set direction to clockwise
    en.off()
    
    # Set delay to maximum speed of motor and rotate fixed number of revolutions
    rev = 20
    
    #Calculate steps
    steps = rev * stepsPerRev

    for x in range(steps):          # rotate one full revolution up checking endstops after steps
        if topEndStop.is_pressed:
            break
        step.on()
        sleep(minDelay)
        step.off()
        sleep(minDelay)


    dir.on()  # switch directions

    for x in range(steps):  # rotate one revolution full checking endstops after steps
        if botEndStop.is_pressed:
            break
        step.on()
        sleep(minDelay)
        step.off()
        sleep(minDelay)
        
    en.on()


