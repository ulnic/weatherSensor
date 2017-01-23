#!/usr/bin/python
import os, subprocess, sys, time, logging
import ConfigParser


logger = logging.getLogger('sensorLogger')


class wifiMon(object):


    def __init__(self, wifiPingHostname="8.8.8.8"):
        self.wifiMonHostname = wifiPingHostname
        logger.info('[wifi Alive check set to] set as: %s', self.wifiMonHostname )


    def keepConnectionAlive(self):
        logger.debug('wifiMon.keepConnectionAlive START')
        
        try:
            cmd = "ping -c 1 -w 5 " + self.wifiMonHostname + " | grep '1 received' "
            p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            out = p.communicate() [0]
            logger.debug( "ping Output = %s", str(out) )

            #and then check the response...  
            if "unreachable" not in out:
            #if out != pingErrorText: # Connection OK
                logger.info("PING to [%s] is Alive", self.wifiMonHostname)
            else: #Connection LOST 
                logger.critical("PING to [%s] is LOST! ", self.wifiMonHostname)
                subprocess.call("sudo ifdown --force wlan0", shell=True)
                subprocess.call("sudo ifup wlan0", shell=True)
        except Exception as e:
            logger.critical('Fatal error in wifiMon! Error: %s', format(e) )

        logger.debug('wifiMon.keepConnectionAlive END')


    def keepWifiAlive(self, wifiCheckFrequency):
        while True:
            self.keepConnectionAlive()
            logger.info("Sleeping thread for [%s] seconds ", wifiCheckFrequency)
            time.sleep(wifiCheckFrequency)


    def setUpLoggingForStandalone():
        global logger
        #Initialise the logger for standalone
        logger = logging.getLogger('sensorLogger')

        logger.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(threadName)-10s - %(message)s')
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(ch)
