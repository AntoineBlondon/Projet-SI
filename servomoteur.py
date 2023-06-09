import sys
import time
import wiringpi
import os

# Parcours : 55 - 240

angle = 140
try:
    angle = int(sys.argv[1])
except:
    pass

def move(angle):
    wiringpi.wiringPiSetupGpio()

    wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)

    # 142,5 = milieu
    wiringpi.pwmWrite(18, angle)

move(200)

"""
delay_period = 0.01

for i in range(3):
    for pulse in range(50, 250, 1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)
    for pulse in range(250, 50, -1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)
"""