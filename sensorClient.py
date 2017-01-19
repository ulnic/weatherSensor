#!/usr/bin/python

import sys, datetime, threading, time, requests
import os, signal, subprocess # This is used when exiting the program
from envSensors import photocell_lib as photocell 
from envSensors.tempHumidity_lib import HTU21D 
import wifiChecker.wifiMon as wifiMon
import logging, logging.config
import ConfigParser
import paho.mqtt.client as mqtt

next_call_Sensors = time.time()
next_call_Wifi = time.time()
reading = HTU21D()
pollingInterval = 30
wifiCheckFrequency = 60
mqtt_host = "127.0.0.1"
config = '' 
MsgTopicAbbreviation = 'weatherSensor'
SensorLocation = 'Room1'
readTemperature=True
messageTopicTemperature = ''
readHumidity=True
messageTopicHumidity = ''
readLight=True
messageTopicLight = ''


###
### Below code KILLS any currently running sensorClient.py process
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
                print "err - could not kill previous running instance"


#Define the Error Log Details
logging.config.fileConfig('logging.ini')
logger = logging.getLogger('sensorLogger')



def setUpConfiguration():
	global config, mqtt_host, wifiCheckFrequency, pollingInterval, readTemperature, readHumidity, readLight
	global SensorLocation, MsgTopicAbbreviation

	config = ConfigParser.ConfigParser()
	try:
		config.read('configuration.ini')
		mqtt_host = config.get('MQTT', 'mqtt_host')
		pollingInterval = int(config.get('DEFAULT', 'pollingInterval'))

		wifiCheckFrequency =  int(config.get('DEFAULT', 'wifiCheckFrequency'))

		readTemperature = bool(config.get('SENSOR', 'readTemperature'))
		readHumidity = bool(config.get('SENSOR', 'readHumidity'))
		readLight = bool(config.get('SENSOR', 'readLight'))
		SensorLocation = config.get('SENSOR', 'SensorLocation')

		MsgTopicAbbreviation = config.get('DEFAULT', 'MsgTopicAbbreviation')

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
 	mqttc.connect(mqtt_host,1883,60)
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

