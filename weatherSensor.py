#!/usr/bin/python
import logging.config
import sys
import threading
import time

from data.ConfigurationReader import ConfigurationReader
from data.SensorHandler import SensorHandler
from data.SingletonExecution import SingletonExecution
from data.wifiChecker.WifiMon import WifiMon as WifiMon

# Define the Error Log Details
logging.config.fileConfig('config/logging.ini')
logger = logging.getLogger('sensorLogger')

# Run a check and close any previously running instances of the same application
SingletonExecution.ensure_only_one_instance()


def update_sensor():

    if ConfigurationReader.readTemperature or ConfigurationReader.readHumidity or ConfigurationReader.readLight:
        sh = SensorHandler(ConfigurationReader.readTemperature, ConfigurationReader.temperatureMessageTopic,
                           ConfigurationReader.temperatureCalibration,
                           ConfigurationReader.readHumidity, ConfigurationReader.humidityMessageTopic,
                           ConfigurationReader.humidityCalibration,
                           ConfigurationReader.readLight, ConfigurationReader.lightMessageTopic,
                           ConfigurationReader.lightCalibration, ConfigurationReader.lightGpioPin,
                           ConfigurationReader.mqtt_host, ConfigurationReader.mqtt_port,
                           ConfigurationReader.useMockSensor,
                           ConfigurationReader.readLocalCPUTemp, ConfigurationReader.localCPUMessageTopic,
                           ConfigurationReader.readIPAddress, ConfigurationReader.localIPMessageTopic)
        t = threading.Thread(name='sensorReaderThread',
                             target=sh.sensor_continuous_reader,
                             args=(ConfigurationReader.polling_interval,))
        t.setDaemon(True)
        t.start()
    else:
        logger.info(" All sensor readers set to FALSE, not executing any sensor readings ")


def monitor_wifi():
    """
    Initiates a thread which will own the execution of the wifi checking and keep alive
    :return:
    """
    wifi_monitor = WifiMon(ConfigurationReader.wifiMonHostname)
    t = threading.Thread(name='wifiMonitorThread',
                         target=wifi_monitor.keep_wifi_alive,
                         args=(ConfigurationReader.wifiCheckFrequency,))
    t.setDaemon(True)
    t.start()


# Main method
def main(argv):
    print 'CTRL+C to break and exit'
    logger.info('***** MQTT SensorCLIENT APPLICATION STARTED *****')
    print argv
    ConfigurationReader()  # Reads the configuration file and stores all values inside it's own class

    try:
        monitor_wifi()  # Sets up the wifi monitor thread
        update_sensor()  # Sets up the monitor sensor & mqtt publishing thread

        while threading.active_count() > 0:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info(" *** RECEIVED TERMINATION AND TERMINATING *** ")
        SensorHandler.threadExitFlag = 1
        sys.exit()


if __name__ == '__main__':
    main(sys.argv)  # Executing the main function
