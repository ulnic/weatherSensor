#!/usr/bin/python

import sys, datetime, threading, time
#import os, signal, subprocess # This is used when exiting the program
#from envSensors import photocell_lib as photocell 
from envSensors import photocell_lib_MOCK as photocell 
#from envSensors.tempHumidity_lib import HTU21D 
from envSensors.tempHumidity_lib_MOCK import HTU21D 
from wifiChecker.wifiMon import wifiMon as WifiMon
#import wifiChecker.wifiMon as WifiMon
import logging, logging.config
import ConfigParser
import paho.mqtt.client as mqtt
from singletonExecution import singletonExecution
#from wifiMon import *

next_call_Sensors = time.time()
next_call_Wifi = time.time()
reading = HTU21D()
pollingInterval = 30
wifiCheckFrequency = 60
wifiMonHostname = "8.8.8.8"
mqtt_host = "127.0.0.1"
mqtt_port = 1883
config = '' 
MsgTopicAbbreviation = 'weatherSensor'
SensorLocation = 'Room1'
readTemperature=True
messageTopicTemperature = ''
readHumidity=True
messageTopicHumidity = ''
readLight=True
messageTopicLight = ''




#Define the Error Log Details
logging.config.fileConfig('logging.ini')
logger = logging.getLogger('sensorLogger')

#Run a check and close any previously running instances of the same application
singletonExecution.ensureOnlyOneInstance()


def setUpConfiguration():
	global config, mqtt_host, mqtt_port, wifiCheckFrequency, pollingInterval, readTemperature, readHumidity, readLight
	global SensorLocation, MsgTopicAbbreviation, wifiMonHostname

	config = ConfigParser.ConfigParser()
	try:
		config.read('configuration.ini')
		mqtt_host = config.get('MQTT', 'mqtt_host')
		mqtt_port = int(config.get('MQTT', 'mqtt_port'))
		pollingInterval = int(config.get('DEFAULT', 'pollingInterval'))

		wifiCheckFrequency =  int(config.get('DEFAULT', 'wifiCheckFrequency'))

		readTemperature = bool(config.get('SENSOR', 'readTemperature'))
		readHumidity = bool(config.get('SENSOR', 'readHumidity'))
		readLight = bool(config.get('SENSOR', 'readLight'))
		SensorLocation = config.get('SENSOR', 'SensorLocation')

		MsgTopicAbbreviation = config.get('DEFAULT', 'MsgTopicAbbreviation')

		wifiMonHostname = config.get('wifiMon', 'wifiMonHostname')

		logger.debug('wifiCheckFrequency is: %s ', wifiCheckFrequency )
	except Exception as e:
		logger.critical('Could NOT read Configuration! Error: %s ', format(e) )

def startup():
	logger.info("CTRL+C to break and exit!")
	monitorWifi()
	readAndSubmitSensorValues()
	

def readAndSubmitSensorValues():
 	global next_call_Sensors, reading, mqtt_host, pollingInterval

 	if(readTemperature):
 		logger.debug("Reading Temperature")
 		temperature = float("{0:.1f}".format(reading.read_temperature()))
 		logger.info("Temperature Reading is: %s", format(temperature))
 	else:
 		 logger.debug("DISABLED: TEMPERATURE read, check the configuration file") 	


 	if(readHumidity):
 		logger.debug("Reading Humidity Sensor")
 		humidity = float("{0:.1f}".format(reading.read_humidity()))
 		logger.info("Humidity Reading is: %s", format(humidity))
 	else:
 		 logger.debug("DISABLED: HUMIDITY read, check the configuration file") 	


 	if(readLight):
 		logger.debug("Reading LIGHT Sensor") 		
 		light = float("{0:.0f}".format(photocell.photocellRead(18)))
 	 	logger.info("Light Reading is: %s", format(light))
 	else:
 		 logger.debug("DISABLED: LIGHT read, check the configuration file") 	



 	logger.debug("MQTT: Initializing")
 	mqttc=mqtt.Client()
 	mqttc.connect(mqtt_host,mqtt_port,60)
 	mqttc.loop_start()
 	
 	logger.debug("MQTT: CONNECTED")

	# SEND MQTT command
	if(readTemperature):
		messageTopic = MsgTopicAbbreviation+"/"+SensorLocation + "/" + "temperature"
		(result,mid)=mqttc.publish(messageTopic,temperature,2)

	if(readHumidity):
		messageTopic = MsgTopicAbbreviation+"/"+SensorLocation + "/" + "humidity"	
 		(result,mid)=mqttc.publish(messageTopic,humidity,2)
 	
 	if(readLight):
 		messageTopic = MsgTopicAbbreviation+"/"+SensorLocation + "/" + "light"
 		(result,mid)=mqttc.publish(messageTopic,light,2)
 
 	logger.debug("MQTT: PUNLISHED ALL 3" )

 	mqttc.loop_stop()
 	mqttc.disconnect()

 	logger.debug("MQTT: CONNECTED")

 	#Get updated polling interval
 	polling_Interval = pollingInterval;
 	next_call_Sensors = next_call_Sensors + int(polling_Interval)
 	#printTime = datetime.datetime.now() + datetime.timedelta(seconds=polling_Interval)
	logger.info("Next run is %s", datetime.datetime.now() + datetime.timedelta(seconds=polling_Interval) )
 	threading.Timer( next_call_Sensors - time.time(), readAndSubmitSensorValues ).start()


def monitorWifi():
	global wifiCheckFrequency
	wifiMonitor = WifiMon(wifiMonHostname)
	t = threading.Thread(name='wifiMonitor', target=wifiMonitor.keepWifiAlive, args=(wifiCheckFrequency,))
	t.start()


# Main method
def main (argv):
	print 'CTRL+C to break and exit'
	logger.info('***** MQTT SensorCLIENT APPLICATION STARTED *****')
	global config, wifiMon

	setUpConfiguration()	# Setup internal configurations reader
	#wifiMon.setupConfiguration(config)   # Setting up the wifi Monitor
	#wifiMon = wifiMon(config)
    
	startup()

if __name__ == '__main__':
	main(sys.argv) # Executing the main funciton

