#!/usr/bin/python
import json
import logging
import threading
import time
import paho.mqtt.publish as publish

from SensorEnum import SensorType
from data.sensors.Sensor import Sensor


logger = logging.getLogger('sensorLogger')

"""
Sensor Handle which initialises all 3 sensors (setup in configuration file)
as well as handles the MQTT publishing.
"""


class SensorHandler(threading.Thread):
    threadExitFlag = 0

    def __init__(self,
                 read_temperature, temperature_message_topic, temperature_calibration,
                 read_humidity, humidity_message_topic, humidity_calibration,
                 read_light, light_message_topic, light_calibration, light_gpio_pin,
                 mqtt_host, mqtt_port,
                 use_mock_sensor,
                 read_cpu, cpu_message_topic,
                 read_ip, ip_message_topic):
        threading.Thread.__init__(self)

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

        self.cpu = Sensor(SensorType.CPU,
                          read_cpu,
                          cpu_message_topic)

        self.ipAdr = Sensor(SensorType.LOCAL_IP,
                            read_ip,
                            ip_message_topic)

        self.mqttHost = mqtt_host
        self.mqttPort = mqtt_port

    # @staticmethod
    # def on_connect(client, userdata, flags, rc):
    #     logger.info("MQTT Connected")
    #
    # def on_disconnect(client, userdata, flags, rc):
    #     logger.info("MQTT DISCONNECTED")

    def read_publish_sensors(self):

        s = [self.temperature, self.humidity, self.light, self.cpu, self.ipAdr]

        for sensor in s:
            sensor.read_sensor()

        data = {}
        data['temperature'] = self.temperature.sensorValue
        data['humidity'] = self.humidity.sensorValue
        data['light'] = self.light.sensorValue
        data['cpu'] = self.cpu.sensorValue
        data['ipAdr'] = self.ipAdr.sensorValue
        json_data = json.dumps(data)

        logger.debug("JSON STRING BUILD: [%s]", json_data.__str__())

        logger.debug("MQTT: Initializing")

        publish.single("weatherSensor/test/rpi", json_data, hostname=self.mqttHost, retain=True,
                       qos=0)

        # try:
        #     mqttc = mqtt.Client()
        #     mqttc.on_connect = self.on_connect
        #     mqttc.on_disconnect = self.on_disconnect
        #     mqttc.connect(self.mqttHost, self.mqttPort, 500)
        #     mqttc.loop_start()
        #
        #     logger.debug("MQTT: CONNECTED")
        #
        #     for sensor in s:
        #         if sensor.readSensorToggle:
        #             sensor.read_sensor()
        #             mqttc.publish(sensor.messageTopic, sensor.sensorValue, 0)
        #             logger.debug("Finished processing [%s]", sensor.type)
        #
        #     logger.debug("MQTT: PUBLISHED")
        #
        #     mqttc.loop_stop()
        #     mqttc.disconnect()
        # except Exception as e:
        #     logger.error("MQTT: Error with %s", e.__str__())

        logger.debug("MQTT: DIS-CONNECTED")

    def sensor_continuous_reader(self, polling_interval):
        while not SensorHandler.threadExitFlag:
            self.read_publish_sensors()
            logger.info("Sleeping SENSOR thread for [%s] seconds ", polling_interval)
            time.sleep(polling_interval)
