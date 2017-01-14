#!/usr/bin/python

# attempt to gather ALL environment readings into 1 file and then execute

import sys, struct, array, time, io, os, fcntl, datetime, sqlite3 as lite
from photocell_lib import photocellRead
from tempHumidity_lib import i2c, HTU21D
from dbHandler import dbPersist

photoCellGPIO = 18

if __name__ == "__main__":
   obj = HTU21D()
   now = datetime.datetime.now()
   temp = obj.read_tmperature()
   humid = obj.read_humidity()
   light = photocellRead(photoCellGPIO)
   out_string = "%d-%02d-%02d %02d:%02d,%.1f,%.1f,%.1f" % (now.year, now.month, now.day, now.hour, now.minute, temp, humid,light)
   print out_string
   dbPersist(temp, humid,light)
