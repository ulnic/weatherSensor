#!/usr/bin/python
import json
import logging
import threading
import time
from data.Constants import Constant
from data.ConfigurationReader import ConfigurationReader
from data.sensors.TemperatureSensor import TemperatureSensor
from data.sensors.HumiditySensor import HumiditySensor
from data.sensors.LightSensor import LightSensor
from data.sensors.IPAddressSensor import IPAddressSensor
from data.sensors.CPUSensor import CPUSensor
from data.MQTTBroker import MQTTBroker

logger = logging.getLogger('sensorLogger')

"""
Sensor Handle which initialises all 3 sensors (setup in configuration file)
as well as handles the MQTT publishing.
"""


class SensorHandler(threading.Thread):
    threadExitFlag = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.cr = ConfigurationReader()
        self.use_mock_sensor = bool(self.cr.get_key_in_section(Constant.CONFIG_SECTION_APP, Constant.USE_MOCK_SENSOR))
        self.polling_interval = int(self.cr.get_key_in_section(Constant.CONFIG_SECTION_APP, Constant.POLLING_INTERVAL))
        self.mqtt = self.create_mqtt_broker()
        self.sensorList = self.create_sensors()

    def read_publish_sensors(self):

        _json = self.read_values_and_generate_json(self.sensorList)
        logger.debug("MQTT: Initializing")
        self.mqtt.publish(_json)
        logger.debug("MQTT: DIS-CONNECTED")

    def sensor_continuous_reader(self):
        _polling_interval = self.polling_interval
        while not SensorHandler.threadExitFlag:
            self.read_publish_sensors()
            logger.info("Sleeping SENSOR thread for [%s] seconds ", _polling_interval)
            time.sleep(_polling_interval)

    def create_mqtt_broker(self):
        keys = self.cr.get_sensor_keys(Constant.CONFIG_SECTION_MQTT)
        mqtt = MQTTBroker(keys[Constant.MQTT_HOST], keys[Constant.MQTT_PORT], keys[Constant.MQTT_TOPIC])
        return mqtt

    def create_sensors(self):

        sensor_list = []
        for sensor in self.cr.get_all_section_names():
            keys = self.cr.get_sensor_keys(sensor)

            # Validate that the config key enable_sensor exist AND is set to TRUE
            _enable_sensor = False
            if Constant.ENABLE_SENSOR in keys and \
                    bool(keys[Constant.ENABLE_SENSOR]) and \
                    keys[Constant.ENABLE_SENSOR].lower() != 'false':
                _enable_sensor = True
                logger.debug('%s  ---  %s', sensor, _enable_sensor.__str__())

            if sensor == Constant.CONFIG_SECTION_TEMPERATURE and _enable_sensor:
                logger.info("Creating TEMP Sensor")
                s = TemperatureSensor(keys[Constant.SENSOR_CALIBRATION], self.use_mock_sensor,
                                      keys[Constant.SENSOR_JSON_KEY])
                sensor_list.append(s)

            elif sensor == Constant.CONFIG_SECTION_HUMIDITY and _enable_sensor:
                logger.info("Creating Humidity Sensor")
                s = HumiditySensor(keys[Constant.SENSOR_CALIBRATION], self.use_mock_sensor,
                                   keys[Constant.SENSOR_JSON_KEY])
                sensor_list.append(s)

            elif sensor == Constant.CONFIG_SECTION_LIGHT and _enable_sensor:
                logger.info("Creating Light Sensor")
                s = LightSensor(keys[Constant.SENSOR_CALIBRATION], self.use_mock_sensor, keys[Constant.SENSOR_JSON_KEY],
                                keys[Constant.SENSOR_GPIO_PIN])
                sensor_list.append(s)

            elif sensor == Constant.CONFIG_SECTION_IP_ADDRESS and _enable_sensor:
                logger.info("Creating IP Address Sensor")
                s = IPAddressSensor(self.use_mock_sensor, keys[Constant.SENSOR_JSON_KEY],
                                    keys[Constant.SENSOR_IP_ADDRESS_INTERFACE])
                sensor_list.append(s)

            elif sensor == Constant.CONFIG_SECTION_CPU and _enable_sensor:
                logger.info("Creating CPU Temp Sensor")
                s = CPUSensor(self.use_mock_sensor, keys[Constant.SENSOR_JSON_KEY])
                sensor_list.append(s)

        if len(sensor_list) == 0:
            logger.warning("*****************************************************************************")
            logger.warning("*** NO SENSOR ADDED. Enable them via the enable_sensor key in the config file")
            logger.warning("*****************************************************************************")
        return sensor_list

    def read_values_and_generate_json(self, _sensor_list):
        data = {}

        try:
            for AbstractSensor in _sensor_list:
                data[AbstractSensor.json_key] = str(AbstractSensor.read_sensor())
        except Exception as e:
            print e.__str__()
            logger.critical("ERROR when creating Sensors. Error was [%s]", e.__str__())

        json_data = json.dumps(data)
        logger.debug("JSON STRING BUILD: [%s]", json_data.__str__())
        return json_data
