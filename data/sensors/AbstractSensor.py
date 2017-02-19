#!/usr/bin/python
"""
Abstract Base Class
"""
import abc


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

