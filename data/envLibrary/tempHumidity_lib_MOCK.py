#!/usr/bin/python
"""
MOCK Temperature Class
"""
import time


# noinspection PyMethodMayBeStatic
class HTU21D(object):
    """
    Mock HTU21D Class
    """
    def __init__(self):
        time.sleep(.1)

    def read_temperature(self):
        """
        MOCK temperature method , always returning fixed value
        :return: 22.2 (always)
        """
        print('*** MOCK TEMPERATURE READING MOCK ***')
        return 22.2

    def read_humidity(self):
        """
        MOCK humidity method , always returning fixed value
        :return: 25.5 (always)
        """
        print('*** MOCK HUMIDITY READING MOCK ***')
        return float(25.5)


# noinspection PyMethodMayBeStatic
class SHT31(object):
    """
    Mock SHT31 Class
    """
    def __init__(self):
        time.sleep(.5)

    def read_temperature(self):
        """
        MOCK temperature method , always returning fixed value
        :return: 18.5 (always)
        """
        print('*** MOCK TEMPERATURE READING MOCK ***')
        return 18.5

    def read_humidity(self):
        """
        MOCK humidity method , always returning fixed value
        :return: 33.3 (always)
        """
        print('*** MOCK HUMIDITY READING MOCK ***')
        return float(33.3)