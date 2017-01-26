#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier versions
# are not fast enough!

import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM)

def photocellRead (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(1)

    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return convertToLinear(reading)


def convertToLinear(p):
    if p > 0:
        return abs(100-(math.log10(p)*30))
    elif p <= 0:
        return 100
    else:
        raise ValueError
