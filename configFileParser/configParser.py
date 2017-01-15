#!/usr/bin/env/python
import sys
import ConfigParser

def readValueHere(config):
    myConfig = config
    print 'inside readValueHere()'
    print config.sections()

print sys.version_info

config = ConfigParser.ConfigParser()
config.read('configuration.ini')

print config.sections()
config.set('dotStar', 'port', '9090')


print config.items('dotStar')
print config.getint('dotStar', 'clockPin')
for key in config.items('dotStar'): print(key)

print 'starting function'

readValueHere(config)
