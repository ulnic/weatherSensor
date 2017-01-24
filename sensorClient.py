#!/usr/bin/python
import time
import sys
import threading
import logging.config
from wifiChecker.WifiMon import WifiMon as WifiMon
from SingletonExecution import SingletonExecution
from ConfigurationReader import ConfigurationReader
from SensorHandler import SensorHandler


# Define the Error Log Details
logging.config.fileConfig('logging.ini')
logger = logging.getLogger('sensorLogger')

# Run a check and close any previously running instances of the same application
SingletonExecution.ensure_only_one_instance()


def update_sensor():
    sh = SensorHandler(ConfigurationReader.readTemperature, ConfigurationReader.temperatureMessageTopic,
                       ConfigurationReader.readHumidity, ConfigurationReader.humidityMessageTopic,
                       ConfigurationReader.readLight, ConfigurationReader.lightMessageTopic,
                       ConfigurationReader.lightGpioPin,
                       ConfigurationReader.mqtt_host, ConfigurationReader.mqtt_port,
                       ConfigurationReader.useMockSensor)
    t = threading.Thread(name='sensorReaderThread',
                         target=sh.sensor_continuous_reader,
                         args=(ConfigurationReader.polling_interval,))
    t.setDaemon(True)
    t.start()


def monitor_wifi():
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
        sys.exit()


if __name__ == '__main__':
    main(sys.argv)  # Executing the main function
