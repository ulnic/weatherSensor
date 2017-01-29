#!/usr/bin/python
import subprocess
import time
import logging
import threading

logger = logging.getLogger('sensorLogger')
WLAN_check_flg = False


class WifiMon(threading.Thread):
    threadExitFlag = 0
    WLAN_check_flg = False

    def __init__(self, wifi_ping_hostname="8.8.8.8"):
        threading.Thread.__init__(self)
        self.wifiMonHostname = wifi_ping_hostname
        logger.info('[wifi Alive check set to] set as: %s', self.wifiMonHostname)

    def keep_wifi_alive(self, wifi_check_frequency):
        while not WifiMon.threadExitFlag:
            self.wlan_check()
            logger.info("Sleeping WIFI thread for [%s] seconds ", wifi_check_frequency)
            time.sleep(wifi_check_frequency)

    def wlan_check(self):

        # This function checks if the WLAN is still up by pinging the router.
        # If there is no return, we'll reset the WLAN connection.
        # If the resetting of the WLAN does not work, we need to reset the Pi.

        ping_ret = subprocess.call(['ping -c 1 -q 192.168.0.200 | grep "1 received" > /dev/null 2> /dev/null'],
                                   shell=True)

        if ping_ret:
            # we lost the WLAN connection.
            # did we try a recovery already?
            if WifiMon.WLAN_check_flg:
                # we have a serious problem and need to reboot the Pi to recover the WLAN connection
                logger.critical(' *** Fatal ERROR in wifi checker *** ')
                logger.critical(' *** After 1 retry, the wifi is NOT available *** ')
                logger.critical(' *** Attempting SUDO REBOOT on Raspberry Pi *** ')
                WifiMon.WLAN_check_flg = False
                subprocess.call(['sudo reboot'], shell=True)
            else:
                # try to recover the connection by resetting the LAN
                logger.critical("PING to [%s] is LOST! ", self.wifiMonHostname)
                logger.critical('Fatal error in wifiMon!')
                logger.critical('ATTEMPTING to turn wifi OFF and ON again!')
                WifiMon.WLAN_check_flg = True  # try to recover
                subprocess.call(['sudo /sbin/ifdown wlan0 && sleep 10 && sudo /sbin/ifup --force wlan0'], shell=True)
        else:
            WifiMon.WLAN_check_flg = False
            logger.info("PING to [%s] is Alive", self.wifiMonHostname)
