#!/usr/bin/python
"""
Entry point into the weather sensor
"""
import logging.config
import sys
import threading
import time

from data.SensorHandler import SensorHandler
import data.SingletonExecution
from data.wifiChecker.WifiMon import WifiMon as WifiMon
from data.Constants import Constant

# Define the Error Log Details
logging.config.fileConfig(Constant.LOGGER_FILE_NAME)
logger = logging.getLogger(Constant.LOGGER_NAME)

# Run a check and close any previously running instances of the same application
data.SingletonExecution.SingletonExecution.ensure_only_one_instance()


def update_sensor():
    """
    Initiates a thread which will validate ALL Sensors and then run them with the frequency defined
    inside the configuration.ini file.
    """
    sh = SensorHandler()
    t = threading.Thread(name='sensorReaderThread', target=sh.sensor_continuous_reader)
    t.setDaemon(True)
    t.start()


def monitor_wifi():
    """
    Initiates a thread which will own the execution of the wifi checking and keep alive
    """
    wifi_monitor = WifiMon()
    t = threading.Thread(name='wifiMonitorThread', target=wifi_monitor.keep_wifi_alive)
    t.setDaemon(True)
    t.start()


def main(argv):
    """
    Start of weatherSensor
    :param argv:
        any command line entries
    """
    print('CTRL+C to break and exit')
    logger.info('*************************************************')
    logger.info('***** MQTT SensorCLIENT APPLICATION STARTED *****')
    logger.info('*************************************************')
    logger.debug('Parameters included on start was [{0}]'.format(argv))
    try:
        monitor_wifi()  # Sets up the wifi monitor thread
        update_sensor()  # Sets up the monitor sensor & mqtt publishing thread

        while threading.active_count() > 0:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info(" ***** RECEIVED TERMINATION AND TERMINATING ***** ")
        SensorHandler.threadExitFlag = 1
        sys.exit()


if __name__ == '__main__':
    main(sys.argv)
