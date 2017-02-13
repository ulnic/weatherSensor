#!/usr/bin/python
import logging
from data.sensors.AbstractSensor import AbstractSensor

logger = logging.getLogger('sensorLogger')


class TemperatureSensor(AbstractSensor):

    #requiredConfig = [Constant.ENABLE_SENSOR, Constant.SENSOR_CALIBRATION, Constant.SENSOR_JSON_KEY]

    def __init__(self, _calibration_value, _use_mock_sensor, _json_key):
        super(self.__class__, self).__init__(_json_key)
        self.calibrationValue = _calibration_value

        if _use_mock_sensor:
            logger.warning("MOCK Readers enabled, please update the configuration file")
            from data.envLibrary.tempHumidity_lib_MOCK import HTU21D
        else:
            logger.debug("LIVE Readers on RPI used.")
            from data.envLibrary.tempHumidity_lib import HTU21D

        self.readSensor = HTU21D()

    def read_sensor(self):
        logger.debug("Reading Temperature Sensor")
        _sensor_reading = float("{0:.1f}".format(self.readSensor.read_temperature() + float(self.calibrationValue)))
        logger.info("Temperature Reading is: %s", format(_sensor_reading))
        return _sensor_reading
