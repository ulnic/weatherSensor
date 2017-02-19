#!/usr/bin/env python
"""
Example for RC timing reading for Raspberry Pi
Must be used with GPIO 0.3.1a or later - earlier version are not fast enough!
"""

import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM)


def read_photocell(_gpio_pin):
    """
    Read the photocell value from the RPI Board, using the specified GPIO Pin.
    :param _gpio_pin: GPIO Pin to read from RPI board
    :return: Read value
    """
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
    """
    Convert log value read to linear
    :param p: reading value to convert
    :return: Converted INT value (now linear instead of log)
    """
    if p > 0:
        return abs(100 - (math.log10(p) * 30))
    elif p <= 0:
        return 100
    else:
        raise ValueError
