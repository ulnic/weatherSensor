#!/usr/bin/python
"""
Wifi Monitoring Class
"""
import logging
import subprocess
import threading
import time
from data.ConfigurationReader import ConfigurationReader
from data.Constants import Constant

logger = logging.getLogger(Constant.LOGGER_NAME)


class WifiMon(threading.Thread):
    """
    Key class handling all WIFI polling / keep alive methods, including the thread which runs to check.
    """
    threadExitFlag = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.cr = ConfigurationReader()

        if not self.cr.has_sensor_section(Constant.CONFIG_SECTION_WIFI):
            logger.fatal("NO WIFI Section found in configuration file. Update Config file and restart")
            raise SystemExit(0)

        self.wifi_ping_host = self.cr.get_key_in_section(Constant.CONFIG_SECTION_WIFI, Constant.WIFI_PING_HOST)
        self.polling_interval = self.cr.get_int_key_in_section(Constant.CONFIG_SECTION_WIFI, Constant.POLLING_INTERVAL)
        self.use_mock_sensor = self.cr.get_bool_key_in_section(Constant.CONFIG_SECTION_APP, Constant.USE_MOCK_SENSOR)
        self.WLAN_check_flg = False

        logger.info('[wifi Alive check set as: {0}'.format(self.wifi_ping_host))

    def keep_wifi_alive(self):
        """
        Function which will be inside its own thread and loops the wifi checker class
        """
        while not WifiMon.threadExitFlag:
            self.wlan_check()
            logger.info("Sleeping WIFI thread for [{0}] seconds ".format(self.polling_interval))
            time.sleep(self.polling_interval)

    def wlan_check(self):
        """
        This function checks if the WLAN is still up by pinging the router.
        If there is no return, we'll reset the WLAN connection.
        If the resetting of the WLAN does not work, we need to reset the Pi.
        :return:
            Positive integer if successful, and negative if unsuccessful as per below
            1 = successful
            -1 = Wifi has failed twice and a SUDO reboot will be created
            -2 = Wifi has failed the first time and a software rpi wifi cycle will be executed.
        """
        if self.use_mock_sensor:
            cmd = 'ping -c 1 -q {0} | grep "1 packets received"'.format(self.wifi_ping_host)
        else:
            cmd = 'ping -c 1 -q {0} | grep "1 received"'.format(self.wifi_ping_host)

        logger.debug(cmd)

        ping_ret = ''
        try:
            ping_ret = subprocess.check_output(cmd, shell=True).rstrip('\n')
        except Exception as cpe:
            logger.critical("Wifi Check failed with [{0}]".format(str(cpe)))

        if len(ping_ret) < 1:
            # we lost the WLAN connection.
            # did we try a recovery already?
            if self.WLAN_check_flg:
                # we have a serious problem and need to reboot the Pi to recover the WLAN connection
                logger.critical(' *** Fatal ERROR in wifi checker *** ')
                logger.critical(' *** After 1 retry, the wifi is NOT available *** ')
                logger.critical(' *** Attempting SUDO REBOOT on Raspberry Pi *** ')
                self.WLAN_check_flg = False
                subprocess.call(['sudo reboot'], shell=True)
                return -1
            else:
                # try to recover the connection by resetting the LAN
                logger.critical("PING to [{0}] is LOST! ".format(self.wifi_ping_host))
                logger.critical('Fatal error in wifiMon!')
                logger.critical('ATTEMPTING to turn wifi OFF and ON again!')
                self.WLAN_check_flg = True  # try to recover
                subprocess.call(['sudo /sbin/ifdown wlan0 && sleep 10 && sudo /sbin/ifup --force wlan0'], shell=True)
                return -2
        else:
            self.WLAN_check_flg = False
            logger.info("PING to [{0}] is Alive".format(self.wifi_ping_host))
            return 1

