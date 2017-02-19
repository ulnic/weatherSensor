#!/usr/bin/python
"""
Class to handle all weather Sensors
"""
import json
import logging
import threading
import time

from Utilities import *
from data.ConfigurationReader import ConfigurationReader
from data.Constants import Constant
from data.MQTTBroker import MQTTBroker
from data.sensors.CPUSensor import CPUSensor
from data.sensors.HumiditySensor import HumiditySensor
from data.sensors.IPAddressSensor import IPAddressSensor
from data.sensors.LightSensor import LightSensor
from data.sensors.TemperatureSensor import TemperatureSensor

logger = logging.getLogger(Constant.LOGGER_NAME)


class SensorHandler(threading.Thread):
    """
    Sensor Handle which initialises all sensors (setup in configuration file)
    """
    threadExitFlag = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.cr = ConfigurationReader()
        self.use_mock_sensor = str_to_bool(
            self.cr.get_key_in_section(Constant.CONFIG_SECTION_APP, Constant.USE_MOCK_SENSOR))
        self.polling_interval = int(self.cr.get_key_in_section(Constant.CONFIG_SECTION_APP, Constant.POLLING_INTERVAL))

        # Creates the MQTT Broker
        keys = self.cr.get_sensor_keys(Constant.CONFIG_SECTION_MQTT)
        self.mqtt = MQTTBroker(keys[Constant.MQTT_HOST], keys[Constant.MQTT_PORT], keys[Constant.MQTT_TOPIC])

        # Create all sensors
        self.sensorList = self.create_sensors()

    def read_publish_sensors(self):
        """
        Creates the json blob by reading all active sensors, and calls the MQTT class to publish
        :return: void
        """
        _json = SensorHandler.read_values_and_generate_json(self.sensorList)
        logger.debug("MQTT: Initializing")
        self.mqtt.publish(_json)
        logger.debug("MQTT: DIS-CONNECTED")

    def sensor_continuous_reader(self):
        """
        Method target to be used in the THREAD which runs and continuously polls the sensor and
        sends data via the MQTT broker.
        :return: void
        """
        _polling_interval = self.polling_interval
        while not SensorHandler.threadExitFlag:
            self.read_publish_sensors()
            logger.info("Sleeping SENSOR thread for [{0}] seconds ".format(_polling_interval))
            time.sleep(_polling_interval)

    def create_sensors(self):
        """
        Validates via the configuration.ini file which sensors are to be made active.
        If they exist, and are set to enable, they will be created.
        :return: List of sensors
        """
        sensor_list = []
        for sensor in self.cr.get_all_section_names():
            keys = self.cr.get_sensor_keys(sensor)

            # Validate that the config key enable_sensor exist AND is set to TRUE
            if Constant.ENABLE_SENSOR in keys and \
                    bool(keys[Constant.ENABLE_SENSOR]) and keys[Constant.ENABLE_SENSOR].lower() != 'false':
                logger.debug('%s  ---  true', sensor)

                if sensor == Constant.CONFIG_SECTION_TEMPERATURE:
                    logger.info("Creating TEMPERATURE Sensor")
                    s = TemperatureSensor(keys[Constant.SENSOR_CALIBRATION], self.use_mock_sensor,
                                          keys[Constant.SENSOR_JSON_KEY])

                elif sensor == Constant.CONFIG_SECTION_HUMIDITY:
                    logger.info("Creating HUMIDITY Sensor")
                    s = HumiditySensor(keys[Constant.SENSOR_CALIBRATION], self.use_mock_sensor,
                                       keys[Constant.SENSOR_JSON_KEY])

                elif sensor == Constant.CONFIG_SECTION_LIGHT:
                    logger.info("Creating LIGHT Sensor")
                    s = LightSensor(keys[Constant.SENSOR_CALIBRATION], self.use_mock_sensor,
                                    keys[Constant.SENSOR_JSON_KEY],
                                    keys[Constant.SENSOR_GPIO_PIN])

                elif sensor == Constant.CONFIG_SECTION_IP_ADDRESS:
                    logger.info("Creating IP Address Sensor")
                    s = IPAddressSensor(self.use_mock_sensor, keys[Constant.SENSOR_JSON_KEY],
                                        keys[Constant.SENSOR_IP_ADDRESS_INTERFACE])

                elif sensor == Constant.CONFIG_SECTION_CPU:
                    logger.info("Creating CPU TEMPERATURE Sensor")
                    s = CPUSensor(self.use_mock_sensor, keys[Constant.SENSOR_JSON_KEY])

                if s is not None:
                    sensor_list.append(s)

        if len(sensor_list) == 0:
            logger.warning("*****************************************************************************")
            logger.warning("*** NO SENSOR ADDED. Enable them via the enable_sensor key in the config file")
            logger.warning("*****************************************************************************")
        return sensor_list

    @staticmethod
    def read_values_and_generate_json(_sensor_list):
        """
        Creates a well formed JSON blob with all sensors values.
        :param _sensor_list: (List) of all sensors to generate the json blob from
        :return: JSON data object with all sensor's already read values
        """
        data = {}

        try:
            for AbstractSensor in _sensor_list:
                logger.debug("Reading {0}".format(AbstractSensor.json_key))
                data[AbstractSensor.json_key] = str(AbstractSensor.read_sensor())
        except Exception as e:
            logger.critical("ERROR when creating Sensors. Error was [{0}]".format(e.__str__()))

        json_data = json.dumps(data)
        logger.debug("JSON STRING BUILD: [{0}]".format(json_data.__str__()))
        return json_data
