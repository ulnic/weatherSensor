#!/usr/bin/python
"""
LIGHT Sensor class
"""
import logging
from data.sensors.AbstractSensor import AbstractSensor
from data.Constants import Constant

logger = logging.getLogger(Constant.LOGGER_NAME)


class LightSensor(AbstractSensor):
    """
    LIGHT Sensor class
    """
    def __init__(self, _calibration_value, _use_mock_sensor, _json_key, _gpio_pin):
        super(self.__class__, self).__init__(_json_key, _use_mock_sensor)
        self.calibrationValue = _calibration_value

        self.gpioPin = _gpio_pin
        if self.use_mock_sensor:
            logger.warning("MOCK Readers enabled, please update the configuration file")
            from data.envLibrary import photocell_lib_MOCK as photo_cell
        else:
            logger.debug("LIVE Readers on RPI used.")
            from data.envLibrary import photocell_lib as photo_cell

        self.photoCellReader = photo_cell

    def read_sensor(self):
        """
        Reads the LIGHT Sensor's light strength value
        :return: the read light level read from sensor
        """
        logger.debug("Reading Light Sensor")
        _sensor_reading = float("{0:.1f}".format(self.photoCellReader.read_photocell(int(self.gpioPin))))
        _calibrate_reading = float("{0:.1f}".format(float(self.calibrationValue)))
        _sensor_value = _sensor_reading + _calibrate_reading
        logger.info("Light Reading is: %s", format(_sensor_value))
        return _sensor_reading
