#!/usr/bin/env python
import random

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier version
# are not fast enough!


def read_photocell(_gpio_pin):
    print('*** MOCK PHOTOCELL READ MOCK ***')
    value = (float(_gpio_pin) * random.randint(1, 10))
    return value
