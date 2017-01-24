#!/bin/bash
cd /home/pi/mqtt_sensor
sleep 10  # Sleeping for 10 seconds to give time for wifi & IP Address to initialise
python sensorClient.py &
echo "*** cron_start.sh executed ***" >> logfile.log
