#!/usr/bin/python
import subprocess
import logging
from data.sensors.AbstractSensor import AbstractSensor

logger = logging.getLogger('sensorLogger')


class IPAddressSensor(AbstractSensor):
    def __init__(self, _use_mock_sensor, _json_key, _interface):
        super(self.__class__, self).__init__(_json_key, _use_mock_sensor)
        self.interface = _interface

    def read_sensor(self):
        logger.debug("Reading IP Address")

        try:
            if self.use_mock_sensor:
                cmd = 'ifconfig ' + self.interface + ' | grep "inet" | cut -d: -f2 | cut -d" " -f2 | grep -v "^$"'
                _ip_address = subprocess.check_output(cmd, shell=True)
                _ip_address = _ip_address.rstrip('\n')
            else:
                cmd = 'ifconfig ' + self.interface + ' | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1 | grep -v "^$"'
            # cmd = 'ifconfig ' + self.interface + ' | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f2 | grep -v "^$"'

                _ip_address = subprocess.check_output(cmd, shell=True)
                _ip_address = _ip_address.rstrip('\n')

            logger.debug('IP ADDRESS RETURNED [%s]', _ip_address)
        except Exception as e:
            logger.warn("Could not read IP, due to: %s", e.__str__())
            _ip_address = 'error'

        logger.info("Local IP Address is %s", _ip_address)

        return _ip_address
