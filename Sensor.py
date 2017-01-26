#!/usr/bin/python
import logging
from SensorEnum import SensorType

logger = logging.getLogger('sensorLogger')


class Sensor(object):
    def __init__(self, sensor_type, read_sensor, sensor_message_topic, calibration_value, use_mock_sensor, gpiopin=-1):
        self.type = sensor_type
        self.readSensorToggle = read_sensor
        self.messageTopic = sensor_message_topic
        self.sensorValue = 0
        self.calibrationValue = calibration_value
        self.useMockSensor = use_mock_sensor
        self.gpioPin = gpiopin

        if use_mock_sensor:
            logger.warning("MOCK Readers enabled, please update the configuration file")
            from envLibrary.tempHumidity_lib_MOCK import HTU21D
            from envLibrary import photocell_lib_MOCK as photocell
        else:
            logger.debug("LIVE Readers on RPI used.")
            from envLibrary.tempHumidity_lib import HTU21D
            from envLibrary import photocell_lib as photocell

        self.readSensor = HTU21D()
        self.photoCellReader = photocell

    def read_sensor(self):
        logger.debug("read Toggle set to %s ", self.readSensorToggle)

        if self.readSensorToggle:
            logger.debug("Reading Sensor")
            if self.type == SensorType.TEMPERATURE:
                self.sensorValue = float("{0:.1f}".format(self.readSensor.read_temperature() + self.calibrationValue))
                logger.info("Temperature Reading is: %s", format(self.sensorValue))

            elif self.type == SensorType.HUMIDITY:
                self.sensorValue = float("{0:.1f}".format(self.readSensor.read_humidity()  + self.calibrationValue))
                logger.info("Humidity Reading is: %s", format(self.sensorValue))

            elif self.type == SensorType.LIGHT:
                self.sensorValue = float("{0:.0f}".format(self.photoCellReader.photocellRead(self.gpioPin) + self.calibrationValue))
                logger.info("Light Reading is: %s", format(self.sensorValue))
        else:
            logger.debug("DISABLED - check the configuration file")

