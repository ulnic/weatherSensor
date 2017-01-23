#!/usr/bin/python
import subprocess
import time
import logging
import threading

logger = logging.getLogger('sensorLogger')


class WifiMon(threading.Thread):

    def __init__(self, wifi_ping_hostname="8.8.8.8"):
        self.wifiMonHostname = wifi_ping_hostname
        logger.info('[wifi Alive check set to] set as: %s', self.wifiMonHostname)

    def stop(self):
        self._Thread__stop()

    def keep_connection_alive(self):
        logger.debug('wifiMon.keepConnectionAlive START')
        
        try:
            cmd = "ping -c 1 -W 5 " + self.wifiMonHostname + " | grep '1 received' "
            logger.debug("ping Output = %s", cmd)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out = p.communicate()[0]
            logger.debug("ping Output = %s", str(out))

            # and then check the response...
            if "unreachable" not in out:
                logger.info("PING to [%s] is Alive", self.wifiMonHostname)
            else:  # Connection LOST
                logger.critical("PING to [%s] is LOST! ", self.wifiMonHostname)
                subprocess.call("sudo ifdown --force wlan0", shell=True)
                subprocess.call("sudo ifup wlan0", shell=True)
        except Exception as e:
            logger.critical('Fatal error in wifiMon! Error: %s', format(e))

        logger.debug('wifiMon.keepConnectionAlive END')

    def keep_wifi_alive(self, wifi_check_frequency):
        while True:
            self.keep_connection_alive()
            logger.info("Sleeping WIFI thread for [%s] seconds ", wifi_check_frequency)
            time.sleep(wifi_check_frequency)
