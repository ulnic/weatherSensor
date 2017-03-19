#!/usr/bin/python
"""
All hardcoded values across weatherSensor is handled here
"""


class Constant(object):
    """
    Each constant holds its unique text, all text values stored here and
    these are used throughout weatherSensor.
    """

    CONFIG_SECTION_APP = 'APP'
    USE_MOCK_SENSOR = 'use_mock_sensor'
    POLLING_INTERVAL = 'polling_interval'

    CONFIG_SECTION_TEMPERATURE = 'SENSOR_TEMPERATURE'
    CONFIG_SECTION_HUMIDITY = 'SENSOR_HUMIDITY'
    CONFIG_SECTION_LIGHT = 'SENSOR_LIGHT'
    CONFIG_SECTION_CPU = 'SENSOR_CPU'
    CONFIG_SECTION_IP_ADDRESS = 'SENSOR_IP_ADDRESS'
    SENSOR_ENABLE = 'sensor_enable'
    SENSOR_CALIBRATION = 'sensor_calibration'
    SENSOR_JSON_KEY = 'sensor_json_key'
    SENSOR_GPIO_PIN = 'sensor_gpio_pin'
    SENSOR_TYPE = 'sensor_type'

    SENSOR_TYPE_OPTION_HTU21D = 'HTU21D'
    SENSOR_TYPE_OPTION_SHT31D = 'SHT31'

    CONFIG_SECTION_MQTT = 'MQTT'
    MQTT_HOST = 'mqtt_host'
    MQTT_PORT = 'mqtt_port'
    MQTT_TOPIC = 'mqtt_topic'

    CONFIG_SECTION_WIFI = 'WIFI'
    SENSOR_IP_ADDRESS_INTERFACE = 'interface'
    WIFI_PING_HOST = 'wifi_ping_host'

    LOGGER_NAME = 'sensorLogger'
    LOGGER_FILE_NAME = 'config/logging.ini'
    CONFIG_FILE_NAME = ['config/configuration.ini', '../config/configuration.ini']

    def __init__(self):
        pass
