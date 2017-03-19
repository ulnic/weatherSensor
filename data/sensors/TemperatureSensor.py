#!/usr/bin/python
"""
Temperature Sensor class
"""
import logging
import sys
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
        self.readSensor = None
        if _sensor_type == Constant.SENSOR_TYPE_OPTION_HTU21D and self.use_mock_sensor:
            logger.warning("HTU21D MOCK Readers enabled, please update the configuration file")
            from data.envLibrary.tempHumidity_lib_MOCK import HTU21D
            self.readSensor = HTU21D()

        elif _sensor_type == Constant.SENSOR_TYPE_OPTION_HTU21D and not self.use_mock_sensor:
            logger.debug("HTU21D LIVE Readers on RPI used.")
            from data.envLibrary.tempHumidity_lib import HTU21D
            self.readSensor = HTU21D()

        elif _sensor_type == Constant.SENSOR_TYPE_OPTION_SHT31D and self.use_mock_sensor:
            logger.warning("SHT31 MOCK Readers enabled, please update the configuration file")
            from data.envLibrary.tempHumidity_lib_MOCK import SHT31
            self.readSensor = SHT31()

        elif _sensor_type == Constant.SENSOR_TYPE_OPTION_HTU21D and not self.use_mock_sensor:
            logger.debug("SHT31 LIVE Readers on RPI used.")
            from data.envLibrary.tempHumidity_lib import SHT31
            self.readSensor = SHT31()

        else:
            logger.debug("FATAL: ONLY HTU21 and SHT31 are Supported. EXITING PROGRAM, PLEASE UPDATE CONFIGURATION.INI")
            print("FATAL: ONLY HTU21 and SHT31 are Supported. EXITING PROGRAM, PLEASE UPDATE CONFIGURATION.INI")
            sys.exit(1)

    def read_sensor(self):
        """
        Reads the TEMPERATURE Sensor's value
        :return: the read temperature value
        """
        logger.debug("Reading Temperature Sensor")
        _sensor_reading = float("{0:.1f}".format(self.readSensor.read_temperature() + float(self.calibrationValue)))
        logger.info("Temperature Reading is: {0}".format(_sensor_reading))
        return _sensor_reading
