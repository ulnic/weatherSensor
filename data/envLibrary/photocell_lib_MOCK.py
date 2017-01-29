#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!


def photocellRead (RCpin):
    print '*** MOCK PHOTOCELL READ MOCK ***'
    return RCpin * 10
