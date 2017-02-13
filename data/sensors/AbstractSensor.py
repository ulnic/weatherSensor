#!/usr/bin/python

import abc


class AbstractSensor(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, _json_key):
        self.json_key = _json_key

    @abc.abstractmethod
    def read_sensor(self):
        return 'Should never see this'
