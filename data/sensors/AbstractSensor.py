#!/usr/bin/python
"""
Abstract Base Class
"""
import abc
import sys
from data.Constants import Constant


class AbstractSensor(object):
    """
    Abstract Base class for all sensors
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, _json_key, _use_mock_sensor):
        self.json_key = _json_key
        self.use_mock_sensor = _use_mock_sensor

    @abc.abstractmethod
    def read_sensor(self):
        """
        Abstract method
        """
        return 'Should never see this'

    @staticmethod
    def setup_senor_hardware_type(_use_mock_sensor, _sensor_type, _logger):
        """
        Setups the hardware sensor type based on what's defined inside configuration.ini.
        :param _logger:
        :param _use_mock_sensor:
        :param _sensor_type:
        """
        if _sensor_type == Constant.SENSOR_TYPE_OPTION_HTU21D and _use_mock_sensor:
            _logger.warning("HTU21D MOCK Readers enabled, please update the configuration file")
            from data.envLibrary.tempHumidity_lib_MOCK import HTU21D
            read_sensor = HTU21D()

        elif _sensor_type == Constant.SENSOR_TYPE_OPTION_HTU21D and not _use_mock_sensor:
            _logger.debug("HTU21D LIVE Readers on RPI used.")
            from data.envLibrary.tempHumidity_lib import HTU21D
            read_sensor = HTU21D()

        elif _sensor_type == Constant.SENSOR_TYPE_OPTION_SHT31D and _use_mock_sensor:
            _logger.warning("SHT31 MOCK Readers enabled, please update the configuration file")
            from data.envLibrary.tempHumidity_lib_MOCK import SHT31
            read_sensor = SHT31()

        elif _sensor_type == Constant.SENSOR_TYPE_OPTION_SHT31D and not _use_mock_sensor:
            _logger.debug("SHT31 LIVE Readers on RPI used.")
            from data.envLibrary.tempHumidity_lib import SHT31
            read_sensor = SHT31()

        else:
            _logger.debug("FATAL: ONLY HTU21 and SHT31 are Supported. EXITING PROGRAM, PLEASE UPDATE CONFIGURATION.INI")
            print("FATAL: ONLY HTU21 and SHT31 are Supported. EXITING PROGRAM, PLEASE UPDATE CONFIGURATION.INI")
            sys.exit(1)

        return read_sensor
