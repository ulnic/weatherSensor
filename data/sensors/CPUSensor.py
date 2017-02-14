#!/usr/bin/python
import logging
from subprocess import check_output

from data.sensors.AbstractSensor import AbstractSensor

logger = logging.getLogger('sensorLogger')


class CPUSensor(AbstractSensor):
    def __init__(self, _use_mock_sensor, _json_key):
        super(self.__class__, self).__init__(_json_key, _use_mock_sensor)

    def read_sensor(self):
        logger.debug("Reading CPU Temperature Sensor")
        _cpu_temp = 0

        try:
            if self.use_mock_sensor:
                _cpu_temp = "temp=40.6'C"
            else:
                _cpu_temp = check_output(["vcgencmd", "measure_temp"])

            _cpu_temp = _cpu_temp.replace("temp=", "").replace("'C", "")
        except Exception as e:
            logger.warn("Could not read CPU, due to %s", e.__str__())

        logger.info("CPU Temperature Reading is %s", _cpu_temp)

        return _cpu_temp
