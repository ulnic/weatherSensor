#!/usr/bin/python
import logging.config
import sys
import threading
import time
from data.SensorHandler import SensorHandler
from data.SingletonExecution import SingletonExecution
from data.wifiChecker.WifiMon import WifiMon as WifiMon

# Define the Error Log Details
logging.config.fileConfig('config/logging.ini')
logger = logging.getLogger('sensorLogger')

# Run a check and close any previously running instances of the same application
SingletonExecution.ensure_only_one_instance()


def update_sensor():
    sh = SensorHandler()
    t = threading.Thread(name='sensorReaderThread', target=sh.sensor_continuous_reader)
    t.setDaemon(True)
    t.start()


def monitor_wifi():
    """
    Initiates a thread which will own the execution of the wifi checking and keep alive
    :return:
    """
    wifi_monitor = WifiMon()
    t = threading.Thread(name='wifiMonitorThread', target=wifi_monitor.keep_wifi_alive)
    t.setDaemon(True)
    t.start()


# Main method
def main(argv):
    print 'CTRL+C to break and exit'
    logger.info('*************************************************')
    logger.info('***** MQTT SensorCLIENT APPLICATION STARTED *****')
    logger.info('*************************************************')

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
    main(sys.argv)  # Executing the main function
