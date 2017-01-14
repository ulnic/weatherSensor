#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!

import RPi.GPIO as GPIO, time, os
import math

DEBUG = 1
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


def convertValueTo100Base(value):
    print 'original value'
    print value
    returnValue = 0;

    if value >= 20000:
        returnValue = 0
    elif value>=15000:
        returnValue = 10
    elif value>=8000:
        returnValue=20
    elif value >=3000:
        returnValue=40
    elif value>=200:
        returnValue=60
    elif value>=70:
        returnValue=80
    else:
        returnValue=100

    return returnValue 
