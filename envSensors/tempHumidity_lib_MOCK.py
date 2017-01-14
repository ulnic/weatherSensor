#!/usr/bin/python
import sys, struct, array, time, io, os, fcntl, datetime

class i2c(object):
   def __init__(self, device, bus):
      string = 'Not implemented'


class HTU21D(object):
   def __init__(self):
      time.sleep(.1)
   
   def read_temperature(self):
      print '*** MOCK TEMPERATURE READING MOCK ***'
      return 23.13468643

         
   def read_humidity(self):
      print '*** MOCK HUMIDITY READING MOCK ***'
      return 60.34527492749342
