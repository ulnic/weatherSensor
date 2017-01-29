#!/usr/bin/python
import logging
import time
import paho.mqtt.client as mqtt

from data.Sensor import Sensor
from data.SensorEnum import SensorType

logger = logging.getLogger('sensorLogger')

"""
Sensor Handle which initialises all 3 sensors (setup in configuration file)
as well as handles the MQTT publishing.
"""


class SensorHandler(object):
    threadExitFlag = 0

    def __init__(self,
                 read_temperature, temperature_message_topic, temperature_calibration,
                 read_humidity, humidity_message_topic, humidity_calibration,
                 read_light, light_message_topic, light_calibration, light_gpio_pin,
                 mqtt_host, mqtt_port,
                 use_mock_sensor):
        self.temperature = Sensor(SensorType.TEMPERATURE,
                                  read_temperature,
                                  temperature_message_topic,
                                  temperature_calibration,
                                  use_mock_sensor)
        self.humidity = Sensor(SensorType.HUMIDITY,
                               read_humidity,
                               humidity_message_topic,
                               humidity_calibration,
                               use_mock_sensor)
        self.light = Sensor(SensorType.LIGHT,
                            read_light,
                            light_message_topic,
                            light_calibration,
                            use_mock_sensor,
                            light_gpio_pin)
        self.mqttHost = mqtt_host
        self.mqttPort = mqtt_port

    def read_publish_sensors(self):

        s = [self.temperature, self.humidity, self.light]

        logger.debug("MQTT: Initializing")
        mqttc = mqtt.Client()
        mqttc.connect(self.mqttHost, self.mqttPort, 60)
        mqttc.loop_start()

        logger.debug("MQTT: CONNECTED")

        for sensor in s:
            if sensor.readSensorToggle:
                sensor.read_sensor()
                mqttc.publish(sensor.messageTopic, sensor.sensorValue, 2)

        logger.debug("MQTT: PUBLISHED")

        mqttc.loop_stop()
        mqttc.disconnect()

        logger.debug("MQTT: DIS-CONNECTED")

    def sensor_continuous_reader(self, polling_interval):
        while not SensorHandler.threadExitFlag:
            self.read_publish_sensors()
            logger.info("Sleeping SENSOR thread for [%s] seconds ", polling_interval)
            time.sleep(polling_interval)
