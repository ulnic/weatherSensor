#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier versions
# are not fast enough!

import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM)


def read_photocell(_gpio_pin):
    reading = 0
    GPIO.setup(_gpio_pin, GPIO.OUT)
    GPIO.output(_gpio_pin, GPIO.LOW)
    time.sleep(1)

    GPIO.setup(_gpio_pin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while GPIO.input(_gpio_pin) == GPIO.LOW:
        reading += 1
    return float(convert_to_linear(reading))


def convert_to_linear(p):
    if p > 0:
        return abs(100 - (math.log10(p) * 30))
    elif p <= 0:
        return 100
    else:
        raise ValueError
