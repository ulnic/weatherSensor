#!/usr/bin/python
"""
All application Context values
"""
import datetime


class AppContext(object):
    """
    Each Application Context value required for weatherSensor
    """

    __last_mqtt_publish = None  # Used to validate if the MQTT has frozen (bad connection)

    def __init__(self):
        pass

    @staticmethod
    def update_last_time():
        """ Resets the last updated MQTT publish with current system date/time stamp"""
        AppContext.__last_mqtt_publish = datetime.datetime.now()

    @staticmethod
    def get_last_updated():
        """ Returns the last stored MQTT Publish timestamp"""
        return AppContext.__last_mqtt_publish

    @staticmethod
    def to_string():
        """ Returns the last stored MQTT Publish timestamp formatted as STRING """
        return AppContext.__last_mqtt_publish.strftime('%Y-%m-%d %H:%M:%S')
