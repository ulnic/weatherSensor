#!/usr/bin/python
import logging
from data.sensors.AbstractSensor import AbstractSensor

logger = logging.getLogger('sensorLogger')


class LightSensor(AbstractSensor):
    def __init__(self, _calibration_value, _use_mock_sensor, _json_key, _gpio_pin):
        super(self.__class__, self).__init__(_json_key)
        self.calibrationValue = _calibration_value

        self.gpioPin = _gpio_pin
        if _use_mock_sensor:
            logger.warning("MOCK Readers enabled, please update the configuration file")
            from data.envLibrary import photocell_lib_MOCK as photocell
        else:
            logger.debug("LIVE Readers on RPI used.")
            from data.envLibrary import photocell_lib as photocell

        self.photoCellReader = photocell

    def read_sensor(self):
        logger.debug("Reading Light Sensor")
        _sensor_reading = float("{:.1f}".format(self.photoCellReader.read_photocell(self.gpioPin) + float(self.calibrationValue)))
        logger.info("Light Reading is: %s", format(_sensor_reading))
        return _sensor_reading
