#!/usr/bin/python
"""
Temperature Sensor class
"""
import logging
import data.sensors.AbstractSensor
from data.Constants import Constant

logger = logging.getLogger(Constant.LOGGER_NAME)


class TemperatureSensor(data.sensors.AbstractSensor.AbstractSensor):
    """
    Temperature Sensor class
    """

    def __init__(self, _calibration_value, _use_mock_sensor, _json_key, _sensor_type):
        super(self.__class__, self).__init__(_json_key, _use_mock_sensor)
        self.calibrationValue = _calibration_value
        self.readSensor = data.sensors.AbstractSensor.AbstractSensor.setup_senor_hardware_type(
            _use_mock_sensor, _sensor_type, logger)

    def read_sensor(self):
        """
        Reads the TEMPERATURE Sensor's value
        :return: the read temperature value
        """
        logger.debug("Reading Temperature Sensor")
        _sensor_reading = float("{0:.1f}".format(self.readSensor.read_temperature() + float(self.calibrationValue)))
        logger.info("Temperature Reading is: {0}".format(_sensor_reading))
        return _sensor_reading
