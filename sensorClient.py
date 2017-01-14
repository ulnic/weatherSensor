#!/usr/bin/python

import sys, datetime, threading, time
import os, signal, subprocess #This is used when exiting the program
from envSensors import photocell_lib as photocell   #MOCK CLASS ADDED HERE
from envSensors.tempHumidity_lib import HTU21D   #MOCK CLASS ADDED HERE
import wifiChecker.wifiMon as wifiMon
import requests
import logging
import logging.config
import ConfigParser
import paho.mqtt.client as mqtt

next_call_Sensors = time.time()
next_call_Wifi = time.time()
reading = HTU21D()
pollingInterval = 30
wifiCheckFrequency = 60
mqtt_host = "127.0.0.1"

###
### Below code KILLS any currently running smartWine.py process
### EXCLUDING itself
###

myPid = os.getpid()
print "My PID= [" + str(myPid) + "]"


cmd = "ps -ef | grep 'python sensorClient.py' | grep -v grep | awk '{print $2}'"
p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
out = p.communicate() [0]
for pid in out.splitlines():
    if myPid != pid:
        #print pid
        if int(pid) != int(myPid):
            try:
                os.kill(int(pid), signal.SIGKILL)
                print "KILLED old sensorClient.py record [" + pid + "]"
            except:
                print "err"
            


#Define the Error Log Details
logging.config.fileConfig('logging.ini')
logger = logging.getLogger('sensorLogger')

config = ''

def setUpConfiguration():
	global config, mqtt_host, wifiCheckFrequency, pollingInterval
	config = ConfigParser.ConfigParser()
	try:
		config.read('configuration.ini')
		mqtt_host = config.get('DEFAULT', 'mqtt_host')
		pollingInterval = int(config.get('DEFAULT', 'pollingInterval'))

		wifiCheckFrequency =  int(config.get('DEFAULT', 'wifiCheckFrequency'))
		logger.debug('wifiCheckFrequency is: %s ', wifiCheckFrequency )
	except Exception as e:
		logger.critical('Could NOT read Configuration! Error: %s ', format(e) )

def startup():
	logger.info("CTRL+C to break and exit!")
	monitorWifi()
	readAndSubmitSensorValues()
	

def readAndSubmitSensorValues():
 	global next_call_Sensors, reading, mqtt_host, pollingInterval
 	# print datetime.datetime.now()

 	#temperature = reading.read_temperature()
 	temperature = float("{0:.1f}".format(reading.read_temperature()))
 	humidity = float("{0:.1f}".format(reading.read_humidity()))
 	light = float("{0:.0f}".format(photocell.photocellRead(18)))
 	# light = photocell.photocellRead(18)

 	logger.info("Temperature Reading is: %s", format(temperature))
 	logger.info("Humidity Reading is: %s", format(humidity))
 	logger.info("Light Reading is: %s", format(light))

 	mqttc=mqtt.Client()
 	mqttc.connect(mqtt_host,1883,60)
 	mqttc.loop_start()
 	
	# SEND MQTT command
 	(result,mid)=mqttc.publish("home-assistant/livingroom/temperature",temperature,2)
 	(result,mid)=mqttc.publish("home-assistant/livingroom/humidity",humidity,2)
 	(result,mid)=mqttc.publish("home-assistant/livingroom/light",light,2)
 	
 	mqttc.loop_stop()
 	mqttc.disconnect()

 	#Get updated polling interval
 	polling_Interval = pollingInterval;
 	next_call_Sensors = next_call_Sensors + int(polling_Interval)
 	printTime = datetime.datetime.now() + datetime.timedelta(seconds=polling_Interval)
	logger.info("Next run is %s",printTime )
 	threading.Timer( next_call_Sensors - time.time(), readAndSubmitSensorValues ).start()


def monitorWifi():
	global next_call_Wifi
	wifiMon.keepConnectionAlive()         # Verify the wifi is still alive. If lost, a reconnection will occur within the method. 
	#Get updated polling interval
 	next_call_Wifi = next_call_Wifi+wifiCheckFrequency # Add time defined inside the configuration.ini (in seconds)
 	threading.Timer( next_call_Wifi - time.time(), monitorWifi ).start()

# Main method
def main (argv):
	print 'CTRL+C to break and exit'
	logger.info('***** MQTT SensorCLIENT APPLICATION STARTED *****')
	global config

	# Setup internal configurations reader
	setUpConfiguration()
	wifiMon.setUp(config)   # Setting up the wifi Monitor
    
	startup()


if __name__ == '__main__':
	main(sys.argv) # Executing the main funciton

