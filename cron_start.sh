#!/bin/bash
cd /home/pi/mqtt_sensor
python sensorClient.py &
echo "*** cron_start.sh executed ***" >> logfile.log
