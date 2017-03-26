#!/usr/bin/python
"""
All application Context values
"""
from data.ConfigurationReader import ConfigurationReader
from data.Constants import Constant


class AppContext(object):
    """
    Each Application Context value required for weatherSensor
    """

    __polling_interval = None  # Polling interval defined in configuration file

    def __init__(self):
        pass

    @staticmethod
    def get_polling_interval():
        """ Returns the polling interval from the configuration file. """
        if AppContext.__polling_interval is None:
            cr = ConfigurationReader()
            AppContext.__polling_interval = cr.get_int_key_in_section(Constant.CONFIG_SECTION_APP,
                                                                      Constant.POLLING_INTERVAL)

        return AppContext.__polling_interval
