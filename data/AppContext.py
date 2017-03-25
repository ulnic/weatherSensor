#!/usr/bin/python
"""
All application Context values
"""
import datetime
from data.ConfigurationReader import ConfigurationReader
from data.Constants import Constant

class AppContext(object):
    """
    Each Application Context value required for weatherSensor
    """

    __last_mqtt_publish = None  # Used to validate if the MQTT has frozen (bad connection)
    __polling_interval = None   # Polling interval defined in configuration file

    def __init__(self):
        pass

    @staticmethod
    def update_last_time():
        """ Resets the last updated MQTT publish with current system date/time stamp"""
        AppContext.__last_mqtt_publish = datetime.datetime.now()

    @staticmethod
    def get_last_updated():
        """ Returns the last stored MQTT Publish timestamp"""

        # To prevent NoneType exception, if never set, we set it the first time only.
        if AppContext.__last_mqtt_publish is None:
            AppContext.update_last_time()

        return AppContext.__last_mqtt_publish


    @staticmethod
    def to_string():
        """ Returns the last stored MQTT Publish timestamp formatted as STRING """
        return AppContext.get_last_updated().strftime('%Y-%m-%d %H:%M:%S')


    @staticmethod
    def get_polling_interval():
        """ Returns the polling interval from the configuration file. """
        if AppContext.__polling_interval is None:
            cr = ConfigurationReader()
            AppContext.__polling_interval = cr.get_int_key_in_section(Constant.CONFIG_SECTION_APP, Constant.POLLING_INTERVAL)

        return AppContext.__polling_interval