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
    temperatureCalibration = 0.0

    readHumidity = True
    humidityMessageTopic = ''
    humidityCalibration = 0.0

    readLight = True
    lightMessageTopic = ''
    lightCalibration = 0.0
    lightGpioPin = -1

    readLocalCPUTemp = True
    localCPUMessageTopic = ''

    readIPAddress = True
    localIPMessageTopic = ''

    def __init__(self):
        logger.debug('ConfigurationReader initialising ')

        logger.info('Reading  configurations from file')
        config = ConfigParser.ConfigParser()
        try:
            config.read('config/configuration.ini')

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
            ConfigurationReader.temperatureCalibration = config.getfloat('SENSOR', 'temperatureCalibration')

            # Humidity Values
            ConfigurationReader.readHumidity = config.getboolean('SENSOR', 'readHumidity')
            ConfigurationReader.humidityMessageTopic = config.get('SENSOR', 'humidityMessageTopic')
            ConfigurationReader.humidityCalibration = config.getfloat('SENSOR', 'humidityCalibration')

            # Light Values
            ConfigurationReader.readLight = config.getboolean('SENSOR', 'readLight')
            ConfigurationReader.lightMessageTopic = config.get('SENSOR', 'lightMessageTopic')
            ConfigurationReader.lightCalibration = config.getfloat('SENSOR', 'lightCalibration')
            ConfigurationReader.lightGpioPin = int(config.get('SENSOR', 'lightGpioPin'))

            # CPU Temperature Values
            ConfigurationReader.readLocalCPUTemp = config.getboolean('SENSOR', 'readLocalCPUTemp')
            ConfigurationReader.localCPUMessageTopic = config.get('SENSOR', 'localCPUMessageTopic')

            # Local IP Address
            ConfigurationReader.readIPAddress = config.getboolean('SENSOR', 'readIPAddress')
            ConfigurationReader.localIPMessageTopic = config.get('SENSOR', 'localIPMessageTopic')

            # WIFI Checking Values
            ConfigurationReader.wifiMonHostname = config.get('WIFI', 'wifiMonHostname')
            ConfigurationReader.wifiCheckFrequency = int(config.get('WIFI', 'wifiCheckFrequency'))

            logger.debug('Finished reading configurations')
        except Exception as e:
            logger.critical('Could NOT read Configuration! Error: %s ', format(e))
