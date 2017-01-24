#!/usr/bin/python
import time


class i2c(object):
    def __init__(self, device, bus):
        string = 'Not implemented'


class HTU21D(object):
    def __init__(self):
        time.sleep(.1)

    def read_temperature(self):
        print '*** MOCK TEMPERATURE READING MOCK ***'
        return 22.2

    def read_humidity(self):
        print '*** MOCK HUMIDITY READING MOCK ***'
        return 55.5
