#!/usr/bin/python
import ConfigParser
import logging

logger = logging.getLogger('sensorLogger')


class ConfigurationReader(object):

    polling_interval = 30
    useMockSensor = False

    wifiCheckFrequency = 60
    wifiMonHostname = "8.8.8.8"

    mqtt_host = "127.0.0.1"
    mqtt_port = 1883

    readTemperature = True
    temperatureMessageTopic = ''

    readHumidity = True
    humidityMessageTopic = ''

    readLight = True
    lightMessageTopic = ''
    lightGpioPin = -1

    def __init__(self):
        logger.debug('ConfigurationReader initialising ')

        logger.info('Reading  configurations from file')
        config = ConfigParser.ConfigParser()
        try:
            config.read('configuration.ini')

            logger.debug(config._sections)

            # Default APPLICATION Values
            ConfigurationReader.polling_interval = int(config.get('APP', 'pollingInterval'))
            ConfigurationReader.useMockSensor = config.getboolean('APP', 'useMockSensor')

            # MQTT Values
            ConfigurationReader.mqtt_host = config.get('MQTT', 'mqtt_host')
            ConfigurationReader.mqtt_port = int(config.get('MQTT', 'mqtt_port'))

            # Temperature Values
            ConfigurationReader.readTemperature = config.getboolean('SENSOR', 'readTemperature')
            ConfigurationReader.temperatureMessageTopic = config.get('SENSOR', 'temperatureMessageTopic')

            # Humidity Values
            ConfigurationReader.readHumidity = config.getboolean('SENSOR', 'readHumidity')
            ConfigurationReader.humidityMessageTopic = config.get('SENSOR', 'humidityMessageTopic')

            # Light Values
            ConfigurationReader.readLight = config.getboolean('SENSOR', 'readLight')
            ConfigurationReader.lightMessageTopic = config.get('SENSOR', 'lightMessageTopic')
            ConfigurationReader.lightGpioPin = int(config.get('SENSOR', 'lightGpioPin'))

            # WIFI Checking Values
            ConfigurationReader.wifiMonHostname = config.get('WIFI', 'wifiMonHostname')
            ConfigurationReader.wifiCheckFrequency = int(config.get('WIFI', 'wifiCheckFrequency'))

            logger.debug('Finished reading configurations')
        except Exception as e:
            logger.critical('Could NOT read Configuration! Error: %s ', format(e))
