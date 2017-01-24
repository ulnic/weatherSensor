#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!

#DEBUG = 1

def photocellRead (RCpin):
    print '*** MOCK PHOTOCELL READ MOCK ***'
    
    return convert_value_to_100_base(250)


def convert_value_to_100_base(value):
#    return_value = 0;

    if value >= 20000:
        return_value = 0
    elif value >= 15000:
        return_value = 10
    elif value >= 8000:
        return_value = 20
    elif value >= 3000:
        return_value = 40
    elif value >= 200:
        return_value = 60
    elif value >= 70:
        return_value = 80
    else:
        return_value = 100

    return return_value
