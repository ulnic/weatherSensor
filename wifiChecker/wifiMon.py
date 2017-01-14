import os
import subprocess
import sys
import logging
import ConfigParser
import time

##
## Define Settings 
##
wifiMonHostname = '' #"8.8.8.8" #Googles DNS Server
logger = logging.getLogger('swLogger')
## END

def setUpLoggingForStandalone():
    global logger
    #Initialise the logger for standalone
    logger = logging.getLogger('swLogger')

    # create logger with 'spam_application'
    logger.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(ch)


def setupConfiguration(config):
    global wifiMonHostname

    logger.debug('wifiMon.setupConfiguration start')

    try:
        logger.debug('Values in configuration are %s', config.items('wifiMon'))
        wifiMonHostname = config.get('wifiMon', 'wifiMonHostname')
    except Exception as e:
    	logger.warning('MISSING Configuration values. Error: %s ', format(e) )
        logger.warning('REVERTING values to pre-defined within wifiMon.setupConfiguration!!!' )
        # set up default values
        wifiMonHostname = "8.8.8.8" #Googles DNS Server

    logger.debug('wifiMon.setupConfiguration end')

#Setup is exectuted from the main smartWine.py class almost like a constructor
def setUp(config):

    setupConfiguration(config)

    logger.debug('wifiMon.setUp start')
    
    logger.debug('wifiMon.setUp end')

def keepConnectionAlive():
    logger.debug('wifiMon.keepAlive START')
    global wifiMonHostname
    try:
        cmd = "ping -c 1 -w 5 " + wifiMonHostname + " | grep '1 received' "
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        out = p.communicate() [0]
        logger.debug( "ping Output = %s", str(out) )

        #and then check the response...  
        if "unreachable" not in out:
        #if out != pingErrorText: # Connection OK
            logger.info("PING to [%s] is Alive", wifiMonHostname)
        else: #Connection LOST 
            logger.critical("PING to [%s] is LOST! ", wifiMonHostname)
            subprocess.call("sudo ifdown --force wlan0", shell=True)
            subprocess.call("sudo ifup wlan0", shell=True)
    except Exception as e:
        logger.critical('Fatal error in wifiMon! Error: %s', format(e) )

	logger.debug('wifiMon.keepAlive END')


def main (argv):
    logger.debug('Number of system Arguments passed in: %s', len(argv) )
    
    
    if(len(argv)>1):
        # This means running standalone and not via smartWine.py
        setUpLoggingForStandalone()
        setUp(None)
        logger.info('Running wifiMon Standalone')
        while True:
            keepAlive()
            time.sleep(5) #Sleep 5 seconds


if __name__ == "__main__":
   main(sys.argv)
