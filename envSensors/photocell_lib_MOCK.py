#!/usr/bin/env python

# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!

import  time, os      

DEBUG = 1

def photocellRead (RCpin):
    print ' *** MOCK PHOTOCELL READ MOCK ***'
    
    return convertValueTo100Base(250)


def convertValueTo100Base(value):
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
