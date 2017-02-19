#!/usr/bin/env python
"""
Example for RC timing reading for Raspberry Pi
Must be used with GPIO 0.3.1a or later - earlier version are not fast enough!
"""
import random


def read_photocell(_gpio_pin):
    """
    Read the photocell value from the RPI Board, using the specified GPIO Pin.
    :param _gpio_pin: GPIO Pin to read from RPI board
    :return: Read value
    """
    print('*** MOCK PHOTOCELL READ MOCK ***')
    value = (float(_gpio_pin) * random.randint(1, 10))
    return value
