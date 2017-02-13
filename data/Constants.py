#!/usr/bin/python


class Constant(object):

    def __init__(self):
        pass

    CONFIG_SECTION_APP = 'APP'
    USE_MOCK_SENSOR = 'use_mock_sensor'
    POLLING_INTERVAL = 'polling_interval'

    CONFIG_SECTION_TEMPERATURE = 'SENSOR_TEMPERATURE'
    CONFIG_SECTION_HUMIDITY = 'SENSOR_HUMIDITY'
    CONFIG_SECTION_LIGHT = 'SENSOR_LIGHT'
    CONFIG_SECTION_CPU = 'SENSOR_CPU'
    CONFIG_SECTION_IP_ADDRESS = 'SENSOR_IP_ADDRESS'
    ENABLE_SENSOR = 'enable_sensor'
    SENSOR_CALIBRATION = 'sensor_calibration'
    SENSOR_JSON_KEY = 'sensor_json_key'
    SENSOR_GPIO_PIN = 'sensor_gpio_pin'

    CONFIG_SECTION_MQTT = 'MQTT'
    MQTT_HOST = 'mqtt_host'
    MQTT_PORT = 'mqtt_port'
    MQTT_TOPIC = 'mqtt_topic'

    CONFIG_SECTION_WIFI = 'WIFI'
    SENSOR_IP_ADDRESS_INTERFACE = 'interface'
    WIFI_PING_HOST = 'wifi_ping_host'
