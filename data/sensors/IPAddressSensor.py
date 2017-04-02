#!/usr/bin/python
"""
IP Address Sensor
"""
import logging
import subprocess
from data.Constants import Constant

from data.sensors.AbstractSensor import AbstractSensor

logger = logging.getLogger(Constant.LOGGER_NAME)


class IPAddressSensor(AbstractSensor):
    """
    IP Address Sensor
    """

    def __init__(self, _use_mock_sensor, _json_key, _interface):
        super(self.__class__, self).__init__(_json_key, _use_mock_sensor)
        self.interface = _interface

    def read_sensor(self):
        """
        Reads the Internal IP Address of its host
        :return: the read IP Address of host where it's running
        """
        logger.debug("Reading IP Address")

        try:
            if self.use_mock_sensor:
                cmd = 'ifconfig {0} | grep "inet" | cut -d: -f2 | cut -d" " -f2 | grep -v "^$"'.format(self.interface)
            else:
                cmd = 'ifconfig {0} | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1 | grep -v "^$"'.format(
                    self.interface)

            _ip_address = subprocess.check_output(cmd, shell=True)
            _ip_address = _ip_address.rstrip('\n')
        except Exception as e:
            logger.warn("Could not read IP, due to: {0}".format(str(e)))
            _ip_address = 'error'

        logger.info("Local IP Address is {0}".format(_ip_address))

        return _ip_address
