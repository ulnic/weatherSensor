#!/bin/bash
cd /home/pi/weatherSensor
sleep 10  # Sleeping for 10 seconds to give time for wifi & IP Address to initialise
python weatherSensor.py &
echo "*** reboot_script_weatherSensor.sh executed ***" >> logs/logfile.log
