#!/usr/bin/python
"""
CPU Sensor
"""
import logging
import subprocess
from data.sensors.AbstractSensor import AbstractSensor
from data.Constants import Constant

logger = logging.getLogger(Constant.LOGGER_NAME)


class CPUSensor(AbstractSensor):
    """
    CPU Sensor class which reads the CPU / GPU sensor of it's host
    """
    def __init__(self, _use_mock_sensor, _json_key):
        super(self.__class__, self).__init__(_json_key, _use_mock_sensor)

    def read_sensor(self):
        """
        Reads the CPU Sensor's temperature value
        :return: the read CPU / GPU temperature value
        """
        logger.debug("Reading CPU Temperature Sensor")
        _cpu_temp = 0

        try:
            if self.use_mock_sensor:
                _cpu_temp = "temp=40.6'C"
            else:
                _cpu_temp = subprocess.check_output(["vcgencmd", "measure_temp"])

            _cpu_temp = _cpu_temp.replace("temp=", "").replace("'C", "").rstrip('\n')
        except Exception as e:
            logger.warn("Could not read CPU, due to {0}".format(str(e)))

        logger.info("CPU Temperature Reading is {0}".format(_cpu_temp))

        return _cpu_temp
